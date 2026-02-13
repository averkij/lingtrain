<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps<{
  html: string
}>()

const emit = defineEmits<{
  refresh: []
}>()
</script>

<template>
  <div class="book-preview">
    <div class="book-preview__header">
      <h3 class="book-preview__title">{{ t('aligner.bookPreview') }}</h3>
      <button class="book-preview__refresh" @click="emit('refresh')">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M11 7a4 4 0 1 1-1.2-2.8M11 2v2.2H8.8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        {{ t('aligner.preview') }}
      </button>
    </div>

    <div v-if="!html" class="book-preview__empty">
      <div class="book-preview__empty-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <span>{{ t('aligner.selectDocument') }}</span>
    </div>

    <!-- eslint-disable vue/no-v-html -->
    <div v-else class="book-preview__content" v-html="html" />
  </div>
</template>

<style scoped>
.book-preview {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-xs);
}

.book-preview__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-md);
}

.book-preview__title {
  font-size: var(--font-size-subsection-title);
  font-weight: 700;
  color: var(--color-text-strong);
}

.book-preview__refresh {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 5px var(--spacing-md);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-primary);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.book-preview__refresh:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.book-preview__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-2xl) var(--spacing-lg);
  color: var(--color-text-muted);
  font-size: var(--font-size-body);
}

.book-preview__empty-icon {
  color: var(--color-border-input);
}

.book-preview__content {
  font-size: var(--font-size-input);
  line-height: 1.7;
  color: var(--color-text);
  max-height: 500px;
  overflow-y: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: var(--spacing-lg);
  background: var(--color-bg-inset);
}
</style>
