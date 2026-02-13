<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useEditorStore } from '@/stores/editor'
import type { ProcessingItem } from '@/api/processing'
import CandidatesList from './CandidatesList.vue'

const { t } = useI18n()
const editor = useEditorStore()

const props = defineProps<{
  item: ProcessingItem
  guid: string
  pageSize: number
}>()

const editingFrom = ref(false)
const editingTo = ref(false)
const editTextFrom = ref('')
const editTextTo = ref('')
const showCandidates = ref(false)
const candidateTextType = ref<'from' | 'to'>('from')
const candidateShift = ref(0)

const lineIdsFrom = computed(() => {
  try { return JSON.parse(props.item.line_id_from) as number[] }
  catch { return [] }
})

const lineIdsTo = computed(() => {
  try { return JSON.parse(props.item.line_id_to) as number[] }
  catch { return [] }
})

function formatLineIds(ids: number[]) {
  if (ids.length === 0) return ''
  if (ids.length === 1) return String(ids[0])
  return `${ids[0]}–${ids[ids.length - 1]}`
}

function startEditFrom() {
  editTextFrom.value = props.item.text_from
  editingFrom.value = true
}

function startEditTo() {
  editTextTo.value = props.item.text_to
  editingTo.value = true
}

async function saveFrom() {
  await editor.editProcessing(props.guid, {
    index_id: props.item.index_id,
    text: editTextFrom.value,
    text_type: 'from',
    operation: 'edit_line',
    batch_id: props.item.batch_id,
    batch_index_id: props.item.batch_index_id,
  })
  editingFrom.value = false
  await editor.fetchProcessingPage(props.guid, props.pageSize, editor.currentPage)
}

async function saveTo() {
  await editor.editProcessing(props.guid, {
    index_id: props.item.index_id,
    text: editTextTo.value,
    text_type: 'to',
    operation: 'edit_line',
    batch_id: props.item.batch_id,
    batch_index_id: props.item.batch_index_id,
  })
  editingTo.value = false
  await editor.fetchProcessingPage(props.guid, props.pageSize, editor.currentPage)
}

function openCandidates(textType: 'from' | 'to') {
  candidateTextType.value = textType
  candidateShift.value = 0
  editor.fetchCandidates(props.guid, textType, props.item.index_id, 3, 3, 0)
  showCandidates.value = true
}

function handleShift(direction: number) {
  candidateShift.value += direction
  editor.fetchCandidates(
    props.guid,
    candidateTextType.value,
    props.item.index_id,
    3,
    3,
    candidateShift.value,
  )
}
</script>

<template>
  <div class="edit-item">
    <div class="edit-item__row">
      <div class="edit-item__top">
        <span class="edit-item__id">{{ item.index_id + 1 }}</span>
      </div>

      <div class="edit-item__sides">
      <!-- From side -->
      <div class="edit-item__side">
        <div class="edit-item__side-header left">
          <span class="edit-item__side-label">{{ t('aligner.from') }}</span>
          <span class="edit-item__line-ids">{{ formatLineIds(lineIdsFrom) }}</span>
        </div>
        <div v-if="!editingFrom" class="edit-item__text" @dblclick="startEditFrom">
          {{ item.text_from || '&mdash;' }}
        </div>
        <div v-else class="edit-item__edit">
          <textarea v-model="editTextFrom" class="edit-item__textarea" rows="3" />
          <div class="edit-item__edit-actions">
            <button class="edit-item__btn edit-item__btn--save" @click="saveFrom">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              OK
            </button>
            <button class="edit-item__btn" @click="editingFrom = false">
              {{ t('aligner.cancel') }}
            </button>
          </div>
        </div>
        <div class="edit-item__tools">
          <button class="edit-item__tool" @click="startEditFrom">{{ t('aligner.editLine') }}</button>
          <button class="edit-item__tool" @click="openCandidates('from')">
            {{ t('aligner.candidates') }}
          </button>
        </div>
      </div>

      <div class="edit-item__divider" />

      <!-- To side -->
      <div class="edit-item__side">
        <div class="edit-item__side-header">
          <span class="edit-item__side-label">{{ t('aligner.to') }}</span>
          <span class="edit-item__line-ids">{{ formatLineIds(lineIdsTo) }}</span>
        </div>
        <div v-if="!editingTo" class="edit-item__text" @dblclick="startEditTo">
          {{ item.text_to || '&mdash;' }}
        </div>
        <div v-else class="edit-item__edit">
          <textarea v-model="editTextTo" class="edit-item__textarea" rows="3" />
          <div class="edit-item__edit-actions">
            <button class="edit-item__btn edit-item__btn--save" @click="saveTo">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              OK
            </button>
            <button class="edit-item__btn" @click="editingTo = false">
              {{ t('aligner.cancel') }}
            </button>
          </div>
        </div>
        <div class="edit-item__tools">
          <button class="edit-item__tool" @click="startEditTo">{{ t('aligner.editLine') }}</button>
          <button class="edit-item__tool" @click="openCandidates('to')">
            {{ t('aligner.candidates') }}
          </button>
        </div>
      </div>
    </div>
    </div>

    <!-- Candidates panel -->
    <CandidatesList
      v-if="showCandidates"
      :candidates="editor.candidates"
      @close="showCandidates = false"
      @shift="handleShift"
    />
  </div>
</template>

<style scoped>
.edit-item {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md) var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-xs);
}

.edit-item:hover {
  border-color: var(--color-border-hover);
}

.edit-item__row {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
}

.edit-item__top {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.edit-item__id {
  font-size: 11px;
  color: var(--color-text-muted-2);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.edit-item__sides {
  flex: 1;
  min-width: 0;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 0;
}

.edit-item__divider {
  width: 1px;
  background: var(--color-border);
  margin: 0 var(--spacing-md);
}

.edit-item__side {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  min-width: 0;
}

.edit-item__side-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: 20px;
}

.edit-item__side-header.left {
  justify-content: flex-end;
}

.edit-item__side-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.edit-item__line-ids {
  font-size: 10px;
  font-weight: 600;
  color: var(--color-primary);
  font-variant-numeric: tabular-nums;
  background: var(--color-primary-subtle, rgba(37, 99, 235, 0.06));
  padding: 1px 6px;
  border-radius: 8px;
}

.edit-item__text {
  font-size: 13px;
  color: var(--color-text);
  line-height: 1.55;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius);
  cursor: text;
  min-height: 20px;
  transition: background var(--transition-fast);
}

.edit-item__text:hover {
  background: var(--color-bg-hover);
}

.edit-item__edit {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.edit-item__textarea {
  width: 100%;
  font-size: 13px;
  color: var(--color-text);
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius);
  padding: var(--spacing-sm);
  resize: vertical;
  font-family: inherit;
  box-sizing: border-box;
  line-height: 1.5;
  transition: border-color var(--transition-fast);
}

.edit-item__textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.edit-item__edit-actions {
  display: flex;
  gap: var(--spacing-xs);
}

.edit-item__tools {
  display: flex;
  gap: var(--spacing-xs);
  flex-wrap: wrap;
}

.edit-item__tool {
  padding: 2px var(--spacing-sm);
  font-size: 11px;
  font-weight: 500;
  color: var(--color-primary);
  background: none;
  border: 1px solid transparent;
  border-radius: var(--radius);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.edit-item__tool:hover {
  background: var(--color-primary-subtle);
  border-color: var(--color-primary);
}

.edit-item__btn {
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 3px var(--spacing-sm);
  font-size: 11px;
  font-weight: 500;
  color: var(--color-text);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.edit-item__btn:hover {
  background: var(--color-bg-hover);
}

.edit-item__btn--save {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.edit-item__btn--save:hover {
  background: var(--color-primary-hover);
}
</style>
