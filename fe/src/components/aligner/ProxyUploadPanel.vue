<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps<{
  label: string
  lang: string
  loaded: boolean
}>()

const emit = defineEmits<{
  upload: [file: File]
}>()

const dragging = ref(false)
const uploading = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

function openFilePicker() {
  fileInput.value?.click()
}

async function handleFile(file: File) {
  uploading.value = true
  try {
    emit('upload', file)
  } finally {
    uploading.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}

function handleFileChange() {
  const file = fileInput.value?.files?.[0]
  if (file) handleFile(file)
}

function handleDrop(e: DragEvent) {
  dragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) handleFile(file)
}
</script>

<template>
  <div class="proxy-panel">
    <div class="proxy-panel__header">
      <h3 class="proxy-panel__title">{{ label }}</h3>
      <span class="proxy-panel__lang">{{ lang.toUpperCase() }}</span>
    </div>

    <div class="proxy-panel__status" :class="{ 'proxy-panel__status--loaded': loaded }">
      {{ loaded ? t('aligner.proxyLoaded') : t('aligner.proxyNotLoaded') }}
    </div>

    <p class="proxy-panel__hint">{{ t('aligner.proxyUploadHint') }}</p>

    <input
      ref="fileInput"
      type="file"
      accept=".txt"
      class="proxy-panel__file-input"
      @change="handleFileChange"
    />

    <div
      class="proxy-panel__dropzone"
      :class="{ 'proxy-panel__dropzone--active': dragging, 'proxy-panel__dropzone--uploading': uploading }"
      @click="openFilePicker"
      @dragenter.prevent="dragging = true"
      @dragover.prevent="dragging = true"
      @dragleave.prevent="dragging = false"
      @drop.prevent="handleDrop"
    >
      <div v-if="uploading" class="proxy-panel__uploading">
        <span class="proxy-panel__spinner" />
        {{ t('aligner.uploading') }}
      </div>
      <div v-else class="proxy-panel__dropzone-content">
        <span class="proxy-panel__dropzone-icon">+</span>
        <span class="proxy-panel__dropzone-text">{{ t('aligner.dropOrClick') }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.proxy-panel {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-xs);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.proxy-panel__header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.proxy-panel__title {
  font-size: var(--font-size-subsection-title);
  font-weight: 700;
  color: var(--color-text-strong);
}

.proxy-panel__lang {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-text-muted);
  background: var(--color-bg-hover);
  padding: 1px 7px;
  border-radius: 10px;
}

.proxy-panel__status {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-muted);
}

.proxy-panel__status--loaded {
  color: var(--color-success);
}

.proxy-panel__hint {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  margin: 0;
  line-height: 1.4;
}

.proxy-panel__file-input {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
}

.proxy-panel__dropzone {
  border: 1.5px dashed var(--color-border-input);
  border-radius: var(--radius);
  padding: var(--spacing-lg) var(--spacing-md);
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.proxy-panel__dropzone:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-subtle);
}

.proxy-panel__dropzone--active {
  border-color: var(--color-primary);
  background: var(--color-primary-subtle);
  border-style: solid;
}

.proxy-panel__dropzone--uploading {
  pointer-events: none;
  opacity: 0.7;
}

.proxy-panel__dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
}

.proxy-panel__dropzone-icon {
  font-size: var(--font-size-icon-lg);
  font-weight: 300;
  color: var(--color-text-muted);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--color-bg-hover);
}

.proxy-panel__dropzone-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.proxy-panel__uploading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-body);
  color: var(--color-primary);
}

.proxy-panel__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
