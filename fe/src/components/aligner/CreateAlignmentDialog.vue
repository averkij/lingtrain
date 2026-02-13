<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAlignerStore } from '@/stores/aligner'
import { listDocuments, type DocumentOut } from '@/api/documents'

const { t } = useI18n()
const aligner = useAlignerStore()

const emit = defineEmits<{
  close: []
  created: []
}>()

const name = ref('')
const documentFromGuid = ref('')
const documentToGuid = ref('')
const docsFrom = ref<DocumentOut[]>([])
const docsTo = ref<DocumentOut[]>([])
const submitting = ref(false)

onMounted(async () => {
  if (aligner.langFrom) {
    docsFrom.value = await listDocuments(aligner.langFrom)
  }
  if (aligner.langTo) {
    docsTo.value = await listDocuments(aligner.langTo)
  }
})

async function handleCreate() {
  if (!name.value || !documentFromGuid.value || !documentToGuid.value) return
  submitting.value = true
  try {
    await aligner.createAlignment({
      name: name.value,
      document_from_guid: documentFromGuid.value,
      document_to_guid: documentToGuid.value,
    })
    emit('created')
    emit('close')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="dialog-overlay" @click.self="emit('close')">
    <div class="dialog">
      <div class="dialog__header">
        <h3 class="dialog__title">{{ t('aligner.createAlignment') }}</h3>
        <button class="dialog__close" @click="emit('close')">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M4 4l6 6M10 4l-6 6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" />
          </svg>
        </button>
      </div>

      <div class="dialog__field">
        <label class="dialog__label">{{ t('aligner.name') }}</label>
        <input v-model="name" type="text" class="dialog__input" :placeholder="t('aligner.name')" />
      </div>

      <div class="dialog__field">
        <label class="dialog__label">{{ t('aligner.documentFrom') }}</label>
        <select v-model="documentFromGuid" class="dialog__select">
          <option value="" disabled>--</option>
          <option v-for="doc in docsFrom" :key="doc.guid" :value="doc.guid">
            {{ doc.name }}
          </option>
        </select>
      </div>

      <div class="dialog__field">
        <label class="dialog__label">{{ t('aligner.documentTo') }}</label>
        <select v-model="documentToGuid" class="dialog__select">
          <option value="" disabled>--</option>
          <option v-for="doc in docsTo" :key="doc.guid" :value="doc.guid">
            {{ doc.name }}
          </option>
        </select>
      </div>

      <div class="dialog__actions">
        <button class="dialog__btn dialog__btn--secondary" @click="emit('close')">
          {{ t('aligner.cancel') }}
        </button>
        <button
          class="dialog__btn dialog__btn--primary"
          :disabled="!name || !documentFromGuid || !documentToGuid || submitting"
          @click="handleCreate"
        >
          {{ submitting ? '...' : t('aligner.createAlignment') }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  animation: fadeIn 0.15s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.dialog {
  background: var(--color-bg-surface);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  width: 420px;
  max-width: 90vw;
  box-shadow: var(--shadow-dialog);
  animation: slideUp 0.2s ease;
}

@keyframes slideUp {
  from { transform: translateY(8px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.dialog__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-lg);
}

.dialog__title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-strong);
  letter-spacing: -0.2px;
}

.dialog__close {
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 4px;
  border-radius: var(--radius);
  display: flex;
  transition: all var(--transition-fast);
}

.dialog__close:hover {
  color: var(--color-text);
  background: var(--color-bg-hover);
}

.dialog__field {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
}

.dialog__label {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.dialog__input,
.dialog__select {
  padding: 8px var(--spacing-md);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius);
  transition: border-color var(--transition-fast);
}

.dialog__input:focus,
.dialog__select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.dialog__actions {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-end;
  margin-top: var(--spacing-lg);
}

.dialog__btn {
  padding: 8px var(--spacing-lg);
  font-size: 13px;
  font-weight: 600;
  border-radius: var(--radius);
  cursor: pointer;
  border: 1px solid transparent;
  transition: all var(--transition-fast);
}

.dialog__btn--primary {
  background: var(--color-primary);
  color: #fff;
}

.dialog__btn--primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.dialog__btn--primary:disabled {
  opacity: 0.4;
  cursor: default;
}

.dialog__btn--secondary {
  background: var(--color-bg-surface);
  color: var(--color-text);
  border-color: var(--color-border);
}

.dialog__btn--secondary:hover {
  background: var(--color-bg-hover);
}
</style>
