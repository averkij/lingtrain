<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import { languages } from '@/i18n'

const appStore = useAppStore()
</script>

<template>
  <button class="language-switcher" @click="appStore.cycleLocale()">
    {{ languages.find((l) => l.code === appStore.locale)?.label }}
  </button>
</template>

<style scoped>
.language-switcher {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  height: 32px;
  padding: 0 var(--spacing-sm);
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius);
  background: transparent;
  color: var(--color-text-subtle);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast);
}

.language-switcher:hover {
  background-color: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}
</style>
