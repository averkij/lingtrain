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
  padding: 0 8px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: transparent;
  color: #374151;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition:
    background-color 0.15s,
    border-color 0.15s;
}

.language-switcher:hover {
  background-color: #f3f4f6;
  border-color: #9ca3af;
}
</style>
