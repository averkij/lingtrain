<script setup lang="ts">
import { ref } from 'vue'
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
const showSplitDialog = ref(false)
const splitPosition = ref(0)
const splitTextType = ref<'from' | 'to'>('from')

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
    index_id: props.item.id,
    text: editTextFrom.value,
    text_type: 'from',
  })
  editingFrom.value = false
  await editor.fetchProcessingPage(props.guid, props.pageSize, editor.currentPage)
}

async function saveTo() {
  await editor.editProcessing(props.guid, {
    index_id: props.item.id,
    text: editTextTo.value,
    text_type: 'to',
  })
  editingTo.value = false
  await editor.fetchProcessingPage(props.guid, props.pageSize, editor.currentPage)
}

function openCandidates(textType: 'from' | 'to') {
  candidateTextType.value = textType
  candidateShift.value = 0
  editor.fetchCandidates(props.guid, textType, props.item.id, 3, 3, 0)
  showCandidates.value = true
}

function handleShift(direction: number) {
  candidateShift.value += direction
  editor.fetchCandidates(
    props.guid,
    candidateTextType.value,
    props.item.id,
    3,
    3,
    candidateShift.value,
  )
}

function openSplit(textType: 'from' | 'to') {
  splitTextType.value = textType
  splitPosition.value = 0
  showSplitDialog.value = true
}

async function handleSplit() {
  await editor.splitSentence(props.guid, {
    index_id: props.item.id,
    text_type: splitTextType.value,
    position: splitPosition.value,
  })
  showSplitDialog.value = false
  await editor.fetchProcessingPage(props.guid, props.pageSize, editor.currentPage)
}

async function handleToggleExcluded() {
  const isExcluded = !!(props.item.meta as Record<string, unknown>)?.excluded
  await editor.toggleExcluded(props.guid, {
    index_id: props.item.id,
    text_type: 'from',
    excluded: !isExcluded,
  })
  await editor.fetchProcessingPage(props.guid, props.pageSize, editor.currentPage)
}

const isExcluded = () => !!(props.item.meta as Record<string, unknown>)?.excluded
</script>

<template>
  <div class="edit-item" :class="{ 'edit-item--excluded': isExcluded() }">
    <div class="edit-item__top">
      <span class="edit-item__id">#{{ item.id }}</span>
      <label class="edit-item__excluded-toggle">
        <input type="checkbox" :checked="isExcluded()" class="edit-item__excluded-input" @change="handleToggleExcluded" />
        <span class="edit-item__excluded-mark" />
        {{ t('aligner.excluded') }}
      </label>
    </div>

    <div class="edit-item__sides">
      <!-- From side -->
      <div class="edit-item__side">
        <div class="edit-item__side-label">{{ t('aligner.from') }}</div>
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
          <button class="edit-item__tool" @click="openSplit('from')">
            {{ t('aligner.split') }}
          </button>
        </div>
      </div>

      <div class="edit-item__divider" />

      <!-- To side -->
      <div class="edit-item__side">
        <div class="edit-item__side-label">{{ t('aligner.to') }}</div>
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
          <button class="edit-item__tool" @click="openSplit('to')">
            {{ t('aligner.split') }}
          </button>
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

    <!-- Split dialog inline -->
    <div v-if="showSplitDialog" class="edit-item__split-dialog">
      <div class="edit-item__split-header">
        <strong>{{ t('aligner.splitSentence') }}</strong>
        <button class="edit-item__split-close" @click="showSplitDialog = false">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M3 3l6 6M9 3l-6 6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" />
          </svg>
        </button>
      </div>
      <div class="edit-item__split-field">
        <label>{{ t('aligner.splitAt') }}</label>
        <input v-model.number="splitPosition" type="number" min="0" class="edit-item__split-input" />
      </div>
      <div class="edit-item__split-actions">
        <button class="edit-item__btn" @click="showSplitDialog = false">
          {{ t('aligner.cancel') }}
        </button>
        <button class="edit-item__btn edit-item__btn--save" @click="handleSplit">
          {{ t('aligner.split') }}
        </button>
      </div>
    </div>
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

.edit-item--excluded {
  opacity: 0.45;
}

.edit-item__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.edit-item__id {
  font-size: 11px;
  color: var(--color-text-muted);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.edit-item__sides {
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

.edit-item__side-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
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

.edit-item__excluded-toggle {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 11px;
  color: var(--color-text-muted);
  cursor: pointer;
  user-select: none;
}

.edit-item__excluded-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.edit-item__excluded-mark {
  width: 14px;
  height: 14px;
  border: 1.5px solid var(--color-border-input);
  border-radius: 3px;
  flex-shrink: 0;
  transition: all var(--transition-fast);
  position: relative;
}

.edit-item__excluded-input:checked + .edit-item__excluded-mark {
  background: var(--color-text-muted);
  border-color: var(--color-text-muted);
}

.edit-item__excluded-input:checked + .edit-item__excluded-mark::after {
  content: '';
  position: absolute;
  left: 3px;
  top: 0px;
  width: 5px;
  height: 8px;
  border: solid #fff;
  border-width: 0 1.5px 1.5px 0;
  transform: rotate(45deg);
}

.edit-item__split-dialog {
  border-top: 1px solid var(--color-border);
  padding-top: var(--spacing-sm);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.edit-item__split-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.edit-item__split-header strong {
  font-size: 12px;
  color: var(--color-text-strong);
}

.edit-item__split-close {
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 2px;
  border-radius: var(--radius);
  display: flex;
}

.edit-item__split-close:hover {
  color: var(--color-text);
  background: var(--color-bg-hover);
}

.edit-item__split-field {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 12px;
  color: var(--color-text-muted);
}

.edit-item__split-input {
  width: 80px;
  padding: 3px var(--spacing-sm);
  font-size: 12px;
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius);
}

.edit-item__split-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.edit-item__split-actions {
  display: flex;
  gap: var(--spacing-xs);
}
</style>
