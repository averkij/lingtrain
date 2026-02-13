<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { AlignmentState, type AlignmentStateValue } from '@/api/alignments'

const { t } = useI18n()

const props = defineProps<{
  state: AlignmentStateValue
}>()

const emit = defineEmits<{
  alignAll: []
  alignNext: []
  stop: []
  resolve: []
}>()

function canStart() {
  return props.state === AlignmentState.INIT || props.state === AlignmentState.IN_PROGRESS_DONE
}

function canAlignNext() {
  return props.state === AlignmentState.INIT || props.state === AlignmentState.IN_PROGRESS_DONE
}

function canStop() {
  return props.state === AlignmentState.IN_PROGRESS
}

function canResolve() {
  return props.state === AlignmentState.IN_PROGRESS_DONE || props.state === AlignmentState.DONE
}
</script>

<template>
  <div class="alignment-controls">
    <h3 class="alignment-controls__title">{{ t('aligner.controls') }}</h3>

    <div class="alignment-controls__buttons">
      <button
        class="alignment-controls__btn alignment-controls__btn--primary"
        disabled
        @click="emit('alignAll')"
      >
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M4 2.5l8 4.5-8 4.5V2.5Z" fill="currentColor" />
        </svg>
        {{ t('aligner.alignAll') }}
      </button>
      <button
        class="alignment-controls__btn"
        :disabled="!canAlignNext()"
        @click="emit('alignNext')"
      >
        {{ t('aligner.alignNext') }}
      </button>
      <button
        class="alignment-controls__btn alignment-controls__btn--danger"
        :disabled="!canStop()"
        @click="emit('stop')"
      >
        {{ t('aligner.stop') }}
      </button>
      <button
        class="alignment-controls__btn"
        :disabled="!canResolve()"
        @click="emit('resolve')"
      >
        {{ t('aligner.resolve') }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.alignment-controls {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-xs);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.alignment-controls__title {
  font-size: var(--font-size-subsection-title);
  font-weight: 700;
  color: var(--color-text-strong);
}

.alignment-controls__buttons {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.alignment-controls__btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 8px var(--spacing-lg);
  font-size: var(--font-size-body);
  font-weight: 500;
  border-radius: var(--radius);
  cursor: pointer;
  border: 1px solid var(--color-border);
  background: var(--color-bg-surface);
  color: var(--color-text);
  transition: all var(--transition-fast);
}

.alignment-controls__btn:hover:not(:disabled) {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.alignment-controls__btn:disabled {
  opacity: 0.35;
  cursor: default;
}

.alignment-controls__btn--primary {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.alignment-controls__btn--primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.alignment-controls__btn--danger {
  color: var(--color-error);
  border-color: currentColor;
}

.alignment-controls__btn--danger:hover:not(:disabled) {
  background: var(--color-error-subtle);
}
</style>
