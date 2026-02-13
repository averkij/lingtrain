<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import type { CandidateLine } from '@/api/processing'

const { t } = useI18n()

defineProps<{
  candidates: CandidateLine[]
}>()

const emit = defineEmits<{
  close: []
  shift: [direction: number]
}>()
</script>

<template>
  <div class="candidates-list">
    <div class="candidates-list__header">
      <h4 class="candidates-list__title">{{ t('aligner.candidates') }}</h4>
      <div class="candidates-list__actions">
        <div class="candidates-list__shift">
          <button class="candidates-list__shift-btn" @click="emit('shift', -1)">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
              <path d="M7 3L4 6l3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="candidates-list__shift-btn" @click="emit('shift', 1)">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
              <path d="M5 3l3 3-3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <button class="candidates-list__close" @click="emit('close')">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M3 3l6 6M9 3l-6 6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" />
          </svg>
        </button>
      </div>
    </div>
    <ul v-if="candidates.length > 0" class="candidates-list__items">
      <li
        v-for="c in candidates"
        :key="c.id"
        class="candidates-list__item"
      >
        <span class="candidates-list__id">#{{ c.index_id }}</span>
        <span class="candidates-list__text">{{ c.text }}</span>
      </li>
    </ul>
    <div v-else class="candidates-list__empty">{{ t('aligner.noDocuments') }}</div>
  </div>
</template>

<style scoped>
.candidates-list {
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: var(--spacing-sm) var(--spacing-md);
  max-height: 200px;
  overflow-y: auto;
  background: var(--color-bg-inset);
}

.candidates-list__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-xs);
}

.candidates-list__title {
  font-size: 11px;
  font-weight: 700;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.candidates-list__actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.candidates-list__shift {
  display: flex;
  gap: 2px;
}

.candidates-list__shift-btn {
  padding: 2px;
  font-size: 12px;
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  cursor: pointer;
  color: var(--color-text-muted);
  display: flex;
  transition: all var(--transition-fast);
}

.candidates-list__shift-btn:hover {
  background: var(--color-bg-hover);
  color: var(--color-text);
}

.candidates-list__close {
  padding: 2px;
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  border-radius: var(--radius);
  display: flex;
  transition: all var(--transition-fast);
}

.candidates-list__close:hover {
  color: var(--color-text);
  background: var(--color-bg-hover);
}

.candidates-list__items {
  list-style: none;
  padding: 0;
  margin: 0;
}

.candidates-list__item {
  display: flex;
  align-items: baseline;
  gap: var(--spacing-xs);
  padding: 3px var(--spacing-xs);
  border-radius: var(--radius);
}

.candidates-list__item:hover {
  background: var(--color-bg-hover);
}

.candidates-list__id {
  font-size: 10px;
  color: var(--color-text-muted);
  flex-shrink: 0;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.candidates-list__text {
  font-size: 12px;
  color: var(--color-text);
  line-height: 1.4;
}

.candidates-list__empty {
  font-size: 12px;
  color: var(--color-text-muted);
  text-align: center;
  padding: var(--spacing-sm);
}
</style>
