<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps<{
  totalPages: number
}>()

const emit = defineEmits<{
  go: [page: number]
  close: []
}>()

const page = ref(1)

function handleGo() {
  const p = Math.max(1, Math.min(page.value, props.totalPages))
  emit('go', p)
  emit('close')
}
</script>

<template>
  <div class="dialog-overlay" @click.self="emit('close')">
    <div class="dialog">
      <div class="dialog__header">
        <h3 class="dialog__title">{{ t('aligner.goToPage') }}</h3>
        <button class="dialog__close" @click="emit('close')">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M4 4l6 6M10 4l-6 6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" />
          </svg>
        </button>
      </div>
      <div class="dialog__field">
        <input
          v-model.number="page"
          type="number"
          :min="1"
          :max="totalPages"
          class="dialog__input"
          @keyup.enter="handleGo"
        />
        <span class="dialog__hint">/ {{ totalPages }}</span>
      </div>
      <div class="dialog__actions">
        <button class="dialog__btn dialog__btn--secondary" @click="emit('close')">
          {{ t('aligner.cancel') }}
        </button>
        <button class="dialog__btn dialog__btn--primary" @click="handleGo">
          {{ t('aligner.go') }}
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
  width: 300px;
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
  font-size: var(--font-size-section-title);
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
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
}

.dialog__input {
  flex: 1;
  padding: 8px var(--spacing-md);
  font-size: var(--font-size-input);
  font-weight: 500;
  color: var(--color-text);
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius);
  transition: border-color var(--transition-fast);
}

.dialog__input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.dialog__hint {
  font-size: var(--font-size-input);
  color: var(--color-text-muted);
  font-weight: 500;
}

.dialog__actions {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-end;
}

.dialog__btn {
  padding: 8px var(--spacing-lg);
  font-size: var(--font-size-body);
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

.dialog__btn--primary:hover {
  background: var(--color-primary-hover);
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
