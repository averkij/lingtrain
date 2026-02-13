<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { uploadDocument, deleteDocument } from '@/api/documents'
import type { DocumentOut } from '@/api/documents'

const { t } = useI18n()

const props = defineProps<{
  lang: string
  documents: DocumentOut[]
  selectedGuid?: string | null
}>()

const emit = defineEmits<{
  select: [doc: DocumentOut]
  changed: []
}>()

const cleanText = ref(false)
const uploading = ref(false)
const dragging = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

function openFilePicker() {
  fileInput.value?.click()
}

async function uploadFile(file: File) {
  uploading.value = true
  try {
    await uploadDocument(props.lang, file, cleanText.value)
    emit('changed')
  } finally {
    uploading.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}

function handleFileChange() {
  const file = fileInput.value?.files?.[0]
  if (file) uploadFile(file)
}

function handleDrop(e: DragEvent) {
  dragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) uploadFile(file)
}

async function handleDelete(guid: string) {
  await deleteDocument(guid)
  emit('changed')
}
</script>

<template>
  <div class="upload-panel">
    <div class="upload-panel__header">
      <h3 class="upload-panel__title">{{ lang.toUpperCase() }}</h3>
      <span class="upload-panel__count">{{ documents.length }}</span>
    </div>

    <input
      ref="fileInput"
      type="file"
      accept=".txt"
      class="upload-panel__file-input"
      @change="handleFileChange"
    />

    <div
      class="upload-panel__dropzone"
      :class="{ 'upload-panel__dropzone--active': dragging, 'upload-panel__dropzone--uploading': uploading }"
      @click="openFilePicker"
      @dragenter.prevent="dragging = true"
      @dragover.prevent="dragging = true"
      @dragleave.prevent="dragging = false"
      @drop.prevent="handleDrop"
    >
      <div v-if="uploading" class="upload-panel__uploading">
        <span class="upload-panel__spinner" />
        {{ t('aligner.uploading') }}
      </div>
      <div v-else class="upload-panel__dropzone-content">
        <span class="upload-panel__dropzone-icon">+</span>
        <span class="upload-panel__dropzone-text">{{ t('aligner.dropOrClick') }}</span>
      </div>
    </div>

    <label class="upload-panel__checkbox">
      <input v-model="cleanText" type="checkbox" class="upload-panel__checkbox-input" />
      <span class="upload-panel__checkbox-mark" />
      {{ t('aligner.cleanText') }}
    </label>

    <ul v-if="documents.length > 0" class="upload-panel__list">
      <li
        v-for="doc in documents"
        :key="doc.guid"
        class="upload-panel__item"
        :class="{ 'upload-panel__item--selected': doc.guid === selectedGuid }"
        @click="emit('select', doc)"
      >
        <div class="upload-panel__item-icon">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M3 1.5h5l3 3v8a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1v-10a1 1 0 0 1 1-1Z" stroke="currentColor" stroke-width="1.2" />
            <path d="M8 1.5v3h3" stroke="currentColor" stroke-width="1.2" />
          </svg>
        </div>
        <span class="upload-panel__name">{{ doc.name }}</span>
        <button
          class="upload-panel__delete"
          :title="t('aligner.delete')"
          @click.stop="handleDelete(doc.guid)"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M4 4l6 6M10 4l-6 6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" />
          </svg>
        </button>
      </li>
    </ul>

    <div v-else class="upload-panel__empty">
      {{ t('aligner.noDocuments') }}
    </div>
  </div>
</template>

<style scoped>
.upload-panel {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-xs);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.upload-panel__header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.upload-panel__title {
  font-size: var(--font-size-subsection-title);
  font-weight: 700;
  color: var(--color-text-strong);
  letter-spacing: 0.5px;
}

.upload-panel__count {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-text-muted);
  background: var(--color-bg-hover);
  padding: 1px 7px;
  border-radius: 10px;
}

.upload-panel__dropzone {
  border: 1.5px dashed var(--color-border-input);
  border-radius: var(--radius);
  padding: var(--spacing-lg) var(--spacing-md);
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.upload-panel__dropzone:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-subtle);
}

.upload-panel__dropzone--active {
  border-color: var(--color-primary);
  background: var(--color-primary-subtle);
  border-style: solid;
}

.upload-panel__dropzone--uploading {
  pointer-events: none;
  opacity: 0.7;
}

.upload-panel__file-input {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
}

.upload-panel__dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
}

.upload-panel__dropzone-icon {
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

.upload-panel__dropzone-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.upload-panel__uploading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-body);
  color: var(--color-primary);
}

.upload-panel__spinner {
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

.upload-panel__checkbox {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  cursor: pointer;
  user-select: none;
}

.upload-panel__checkbox-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.upload-panel__checkbox-mark {
  width: 16px;
  height: 16px;
  border: 1.5px solid var(--color-border-input);
  border-radius: 4px;
  flex-shrink: 0;
  transition: all var(--transition-fast);
  position: relative;
}

.upload-panel__checkbox-input:checked + .upload-panel__checkbox-mark {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.upload-panel__checkbox-input:checked + .upload-panel__checkbox-mark::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 1px;
  width: 5px;
  height: 9px;
  border: solid #fff;
  border-width: 0 1.5px 1.5px 0;
  transform: rotate(45deg);
}

.upload-panel__list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.upload-panel__item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-sm);
  border-radius: var(--radius);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.upload-panel__item:hover {
  background: var(--color-bg-hover);
}

.upload-panel__item--selected {
  background: var(--color-primary-subtle);
  border-left: 2px solid var(--color-primary);
  padding-left: calc(var(--spacing-sm) - 2px);
}

.upload-panel__item--selected .upload-panel__name {
  color: var(--color-primary);
  font-weight: 600;
}

.upload-panel__item-icon {
  color: var(--color-text-muted);
  flex-shrink: 0;
  display: flex;
}

.upload-panel__name {
  font-size: var(--font-size-body);
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.upload-panel__delete {
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 2px;
  border-radius: var(--radius);
  display: flex;
  opacity: 0;
  transition: all var(--transition-fast);
}

.upload-panel__item:hover .upload-panel__delete {
  opacity: 1;
}

.upload-panel__delete:hover {
  color: var(--color-error);
  background: var(--color-error-subtle);
}

.upload-panel__empty {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  text-align: center;
  padding: var(--spacing-md);
}
</style>
