<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const batchSize = defineModel<number>('batchSize', { required: true })
const batchCount = defineModel<number>('batchCount', { required: true })
const window = defineModel<number>('window', { required: true })
const batchShift = defineModel<number>('batchShift', { required: true })
const useProxyFrom = defineModel<boolean>('useProxyFrom', { required: true })
const useProxyTo = defineModel<boolean>('useProxyTo', { required: true })
</script>

<template>
  <div class="alignment-settings">
    <h3 class="alignment-settings__title">{{ t('aligner.settings') }}</h3>

    <div class="alignment-settings__grid">
      <div class="alignment-settings__field">
        <label class="alignment-settings__label">{{ t('aligner.batchSize') }}</label>
        <input v-model.number="batchSize" type="number" min="1" disabled class="alignment-settings__input" />
      </div>
      <div class="alignment-settings__field">
        <label class="alignment-settings__label">{{ t('aligner.batchCount') }}</label>
        <input v-model.number="batchCount" type="number" min="1" max="5" class="alignment-settings__input" />
      </div>
      <div class="alignment-settings__field">
        <label class="alignment-settings__label">{{ t('aligner.window') }}</label>
        <input v-model.number="window" type="number" min="1" class="alignment-settings__input" />
      </div>
      <div class="alignment-settings__field">
        <label class="alignment-settings__label">{{ t('aligner.batchShift') }}</label>
        <div class="alignment-settings__shift-row">
          <input v-model.number="batchShift" type="range" min="-200" max="200" step="10" class="alignment-settings__slider" />
          <span class="alignment-settings__slider-value">{{ batchShift }}</span>
          <button class="alignment-settings__reset-btn" :title="'Reset'" @click="batchShift = 0">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M2.5 2.5v3.5h3.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M2.8 6A4.5 4.5 0 1 1 3.5 9" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div class="alignment-settings__checkboxes">
      <label class="alignment-settings__checkbox">
        <input v-model="useProxyFrom" type="checkbox" class="alignment-settings__checkbox-input" />
        <span class="alignment-settings__checkbox-mark" />
        {{ t('aligner.useProxyFrom') }}
      </label>
      <label class="alignment-settings__checkbox">
        <input v-model="useProxyTo" type="checkbox" class="alignment-settings__checkbox-input" />
        <span class="alignment-settings__checkbox-mark" />
        {{ t('aligner.useProxyTo') }}
      </label>
    </div>
  </div>
</template>

<style scoped>
.alignment-settings {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-xs);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.alignment-settings__title {
  font-size: var(--font-size-subsection-title);
  font-weight: 700;
  color: var(--color-text-strong);
}

.alignment-settings__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.alignment-settings__field {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.alignment-settings__label {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.alignment-settings__input {
  padding: 7px var(--spacing-md);
  font-size: var(--font-size-input);
  font-weight: 500;
  color: var(--color-text);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius);
  width: 100%;
  box-sizing: border-box;
  transition: border-color var(--transition-fast);
}

.alignment-settings__input:disabled {
  opacity: 0.5;
  cursor: default;
}

.alignment-settings__input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.alignment-settings__shift-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  height: 35px;
}

.alignment-settings__slider {
  flex: 1;
  height: 4px;
  accent-color: var(--color-primary);
  cursor: pointer;
}

.alignment-settings__slider-value {
  font-size: var(--font-size-body);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: var(--color-text);
  min-width: 36px;
  text-align: right;
}

.alignment-settings__reset-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  padding: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-bg-surface);
  color: var(--color-text-muted);
  cursor: pointer;
  flex-shrink: 0;
  transition: all var(--transition-fast);
}

.alignment-settings__reset-btn:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
  background: var(--color-primary-subtle);
}

.alignment-settings__checkboxes {
  display: flex;
  gap: var(--spacing-lg);
}

.alignment-settings__checkbox {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-body);
  color: var(--color-text);
  cursor: pointer;
  user-select: none;
}

.alignment-settings__checkbox-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.alignment-settings__checkbox-mark {
  width: 16px;
  height: 16px;
  border: 1.5px solid var(--color-border-input);
  border-radius: 4px;
  flex-shrink: 0;
  transition: all var(--transition-fast);
  position: relative;
}

.alignment-settings__checkbox-input:checked + .alignment-settings__checkbox-mark {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.alignment-settings__checkbox-input:checked + .alignment-settings__checkbox-mark::after {
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
</style>
