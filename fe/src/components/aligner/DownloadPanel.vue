<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useEditorStore } from '@/stores/editor'

const { t } = useI18n()
const editor = useEditorStore()

const props = defineProps<{
  guid: string
  format: string
  theme: string
}>()

function triggerDownload(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

async function handleDownloadProcessing() {
  const blob = await editor.downloadProcessing(props.guid, { format: props.format })
  triggerDownload(blob, `${props.guid}_processing.${props.format}`)
}

async function handleDownloadBook() {
  const blob = await editor.downloadBook(props.guid, {
    format: props.format,
    theme: props.theme !== 'none' ? props.theme : undefined,
  })
  triggerDownload(blob, `${props.guid}_book.${props.format}`)
}
</script>

<template>
  <div class="download-panel">
    <h3 class="download-panel__title">{{ t('aligner.download') }}</h3>
    <div class="download-panel__buttons">
      <button class="download-panel__btn" @click="handleDownloadProcessing">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M7 2v7M4 6.5L7 9.5l3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M2 11h10" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
        </svg>
        {{ t('aligner.downloadProcessing') }}
      </button>
      <button class="download-panel__btn download-panel__btn--primary" @click="handleDownloadBook">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M7 2v7M4 6.5L7 9.5l3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M2 11h10" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
        </svg>
        {{ t('aligner.downloadBook') }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.download-panel {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-xs);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.download-panel__title {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-strong);
}

.download-panel__buttons {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.download-panel__btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 8px var(--spacing-lg);
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius);
  cursor: pointer;
  border: 1px solid var(--color-border);
  background: var(--color-bg-surface);
  color: var(--color-text);
  transition: all var(--transition-fast);
}

.download-panel__btn:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.download-panel__btn--primary {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.download-panel__btn--primary:hover {
  background: var(--color-primary-hover);
}
</style>
