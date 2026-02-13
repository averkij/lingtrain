<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps<{
  currentPage: number
  totalPages: number
}>()

const emit = defineEmits<{
  pageChange: [page: number]
}>()

function prev() {
  if (props.currentPage > 1) emit('pageChange', props.currentPage - 1)
}

function next() {
  if (props.currentPage < props.totalPages) emit('pageChange', props.currentPage + 1)
}
</script>

<template>
  <div class="pagination">
    <button class="pagination__btn" :disabled="currentPage <= 1" @click="prev">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M8 3L5 7l3 4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      {{ t('aligner.prev') }}
    </button>
    <span class="pagination__info">{{ currentPage }} / {{ totalPages }}</span>
    <button class="pagination__btn" :disabled="currentPage >= totalPages" @click="next">
      {{ t('aligner.next') }}
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M6 3l3 4-3 4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
}

.pagination__btn {
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 5px var(--spacing-md);
  font-size: 12px;
  font-weight: 500;
  color: var(--color-primary);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.pagination__btn:hover:not(:disabled) {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.pagination__btn:disabled {
  color: var(--color-text-muted);
  cursor: default;
  opacity: 0.5;
}

.pagination__info {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  min-width: 60px;
  text-align: center;
  font-variant-numeric: tabular-nums;
}
</style>
