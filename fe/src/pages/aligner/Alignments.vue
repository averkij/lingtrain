<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAlignerStore } from '@/stores/aligner'
import { AlignmentState } from '@/api/alignments'
import CreateAlignmentDialog from '@/components/aligner/CreateAlignmentDialog.vue'

const { t } = useI18n()
const router = useRouter()
const aligner = useAlignerStore()

const showCreateDialog = ref(false)

const stateLabels: Record<number, string> = {
  [AlignmentState.INIT]: 'aligner.stateInit',
  [AlignmentState.IN_PROGRESS]: 'aligner.stateInProgress',
  [AlignmentState.IN_PROGRESS_DONE]: 'aligner.stateInProgressDone',
  [AlignmentState.DONE]: 'aligner.stateDone',
  [AlignmentState.ERROR]: 'aligner.stateError',
}

onMounted(() => {
  aligner.fetchAlignments()
})

function openDetail(guid: string) {
  router.push({ name: 'aligner-alignment-detail', params: { guid } })
}

async function handleDelete(guid: string) {
  await aligner.deleteAlignment(guid)
}
</script>

<template>
  <div class="aligner-alignments">
    <div class="aligner-alignments__header">
      <h1>{{ t('aligner.alignments') }}</h1>
      <button class="aligner-alignments__create-btn" @click="showCreateDialog = true">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M7 2v10M2 7h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
        </svg>
        {{ t('aligner.createAlignment') }}
      </button>
    </div>

    <div v-if="aligner.loading" class="aligner-alignments__loading">
      <span class="aligner-alignments__spinner" />
      {{ t('aligner.loading') }}
    </div>

    <div v-else-if="aligner.alignments.length === 0" class="aligner-alignments__empty">
      <div class="aligner-alignments__empty-icon">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <rect x="4" y="6" width="24" height="20" rx="3" stroke="currentColor" stroke-width="1.5" />
          <path d="M4 14h24" stroke="currentColor" stroke-width="1.5" />
          <path d="M16 6v20" stroke="currentColor" stroke-width="1.5" />
        </svg>
      </div>
      {{ t('aligner.noAlignments') }}
    </div>

    <ul v-else class="aligner-alignments__list">
      <li
        v-for="a in aligner.alignments"
        :key="a.guid"
        class="aligner-alignments__item"
        @click="openDetail(a.guid)"
      >
        <div class="aligner-alignments__item-main">
          <span class="aligner-alignments__item-name">{{ a.name }}</span>
          <span class="aligner-alignments__item-langs">{{ a.lang_from }} &rarr; {{ a.lang_to }}</span>
        </div>
        <div class="aligner-alignments__item-right">
          <span
            class="aligner-alignments__state"
            :class="`aligner-alignments__state--${a.state}`"
          >
            {{ t(stateLabels[a.state] ?? 'aligner.stateInit') }}
          </span>
          <div v-if="a.total_batches > 0" class="aligner-alignments__mini-progress">
            <div
              class="aligner-alignments__mini-progress-fill"
              :style="{ width: `${(a.curr_batches / a.total_batches) * 100}%` }"
            />
          </div>
          <button
            class="aligner-alignments__delete"
            :title="t('aligner.delete')"
            @click.stop="handleDelete(a.guid)"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M4 4l6 6M10 4l-6 6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" />
            </svg>
          </button>
        </div>
      </li>
    </ul>

    <CreateAlignmentDialog
      v-if="showCreateDialog"
      @close="showCreateDialog = false"
      @created="aligner.fetchAlignments()"
    />
  </div>
</template>

<style scoped>
.aligner-alignments {
  padding: var(--spacing-xl) 0;
}

.aligner-alignments__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-xl);
}

h1 {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-strong);
  margin: 0;
  letter-spacing: -0.3px;
}

.aligner-alignments__create-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 8px var(--spacing-lg);
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  background: var(--color-primary);
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background var(--transition-fast);
  box-shadow: var(--shadow-xs);
}

.aligner-alignments__create-btn:hover {
  background: var(--color-primary-hover);
}

.aligner-alignments__loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: 13px;
  color: var(--color-text-muted);
  padding: var(--spacing-2xl);
}

.aligner-alignments__spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.aligner-alignments__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  font-size: 13px;
  color: var(--color-text-muted);
  text-align: center;
  padding: var(--spacing-2xl);
}

.aligner-alignments__empty-icon {
  color: var(--color-border-input);
}

.aligner-alignments__list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.aligner-alignments__item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-xs);
}

.aligner-alignments__item:hover {
  border-color: var(--color-border-hover);
  box-shadow: var(--shadow-sm);
}

.aligner-alignments__item-main {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.aligner-alignments__item-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
}

.aligner-alignments__item-langs {
  font-size: 12px;
  color: var(--color-text-muted);
  font-weight: 500;
}

.aligner-alignments__item-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.aligner-alignments__state {
  padding: 3px 10px;
  font-size: 11px;
  font-weight: 600;
  border-radius: 20px;
  white-space: nowrap;
  letter-spacing: 0.2px;
}

.aligner-alignments__state--0 {
  background: var(--color-bg-hover);
  color: var(--color-text-muted);
}
.aligner-alignments__state--1 {
  background: var(--color-info-subtle);
  color: #1d4ed8;
}
.aligner-alignments__state--2 {
  background: var(--color-warning-subtle);
  color: var(--color-warning);
}
.aligner-alignments__state--3 {
  background: var(--color-success-subtle);
  color: var(--color-success);
}
.aligner-alignments__state--4 {
  background: var(--color-error-subtle);
  color: var(--color-error);
}

.aligner-alignments__mini-progress {
  width: 64px;
  height: 4px;
  background: var(--color-bg-hover);
  border-radius: 2px;
  overflow: hidden;
}

.aligner-alignments__mini-progress-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 2px;
  transition: width var(--transition-normal);
}

.aligner-alignments__delete {
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 4px;
  border-radius: var(--radius);
  display: flex;
  opacity: 0;
  transition: all var(--transition-fast);
}

.aligner-alignments__item:hover .aligner-alignments__delete {
  opacity: 1;
}

.aligner-alignments__delete:hover {
  color: var(--color-error);
  background: var(--color-error-subtle);
}
</style>
