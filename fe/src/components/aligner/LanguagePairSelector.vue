<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const langFrom = defineModel<string>('langFrom', { required: true })
const langTo = defineModel<string>('langTo', { required: true })

const languageCodes = [
  'en', 'ru', 'de', 'fr', 'es', 'pt', 'it', 'nl', 'pl', 'sv', 'da', 'nb', 'fi',
  'uk', 'be', 'cs', 'sk', 'bg', 'hr', 'sl', 'sr', 'mk', 'bs', 'ro', 'hu', 'tr',
  'el', 'ka', 'hy', 'az', 'kk', 'uz', 'tg', 'ky', 'tt', 'ba', 'cv', 'mn',
  'zh', 'ja', 'ko', 'vi', 'th', 'hi', 'bn', 'ta', 'te', 'ml', 'ur',
  'ar', 'he', 'fa', 'id', 'ms', 'tl', 'sw', 'am', 'yo', 'ig', 'ha', 'zu', 'xh',
  'af', 'sq', 'lt', 'lv', 'et', 'la', 'eo', 'cu', 'xx',
]
</script>

<template>
  <div class="lang-pair-selector">
    <div class="lang-pair-selector__field">
      <label class="lang-pair-selector__label">{{ t('aligner.langFrom') }}</label>
      <select v-model="langFrom" class="lang-pair-selector__select">
        <option v-for="code in languageCodes" :key="code" :value="code">{{ code }}</option>
      </select>
    </div>
    <div class="lang-pair-selector__arrow">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M3 8h10M10 5l3 3-3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <div class="lang-pair-selector__field">
      <label class="lang-pair-selector__label">{{ t('aligner.langTo') }}</label>
      <select v-model="langTo" class="lang-pair-selector__select">
        <option v-for="code in languageCodes" :key="code" :value="code">{{ code }}</option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.lang-pair-selector {
  display: flex;
  align-items: flex-end;
  gap: var(--spacing-md);
}

.lang-pair-selector__field {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.lang-pair-selector__label {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.lang-pair-selector__select {
  padding: 7px var(--spacing-md);
  font-size: var(--font-size-input);
  font-weight: 500;
  color: var(--color-text);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius);
  cursor: pointer;
  min-width: 80px;
  transition: border-color var(--transition-fast);
}

.lang-pair-selector__select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.lang-pair-selector__arrow {
  color: var(--color-text-muted);
  padding-bottom: 8px;
  display: flex;
}
</style>
