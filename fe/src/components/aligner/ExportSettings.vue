<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const format = defineModel<string>('format', { required: true })
const theme = defineModel<string>('theme', { required: true })

const formats = ['tmx', 'xml', 'json', 'txt', 'db']
const themes = ['none', 'default']
</script>

<template>
  <div class="export-settings">
    <h3 class="export-settings__title">{{ t('aligner.export') }}</h3>

    <div class="export-settings__field">
      <label class="export-settings__label">{{ t('aligner.format') }}</label>
      <select v-model="format" class="export-settings__select">
        <option v-for="f in formats" :key="f" :value="f">{{ f.toUpperCase() }}</option>
      </select>
    </div>

    <div class="export-settings__field">
      <label class="export-settings__label">{{ t('aligner.theme') }}</label>
      <select v-model="theme" class="export-settings__select">
        <option v-for="th in themes" :key="th" :value="th">{{ th }}</option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.export-settings {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-xs);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.export-settings__title {
  font-size: var(--font-size-body);
  font-weight: 700;
  color: var(--color-text-strong);
}

.export-settings__field {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.export-settings__label {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.export-settings__select {
  padding: 7px var(--spacing-md);
  font-size: var(--font-size-input);
  font-weight: 500;
  color: var(--color-text);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius);
  cursor: pointer;
  transition: border-color var(--transition-fast);
}

.export-settings__select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}
</style>
