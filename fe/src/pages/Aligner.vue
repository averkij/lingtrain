<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'

const { t } = useI18n()
const route = useRoute()

const tabs = [
  { name: 'aligner-documents', label: () => t('aligner.documents') },
  { name: 'aligner-alignments', label: () => t('aligner.alignments'), matchNames: ['aligner-alignment-detail'] },
  { name: 'aligner-create', label: () => t('aligner.create') },
]

function isTabActive(tab: typeof tabs[number]) {
  const currentName = route.name as string
  if (currentName === tab.name) return true
  return tab.matchNames?.includes(currentName) ?? false
}
</script>

<template>
  <div class="aligner-page">
    <nav class="aligner-tabs">
      <RouterLink
        v-for="tab in tabs"
        :key="tab.name"
        :to="{ name: tab.name }"
        class="aligner-tab"
        :class="{ 'aligner-tab--active': isTabActive(tab) }"
      >
        {{ tab.label() }}
      </RouterLink>
    </nav>
    <div class="aligner-content">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.aligner-page {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.aligner-tabs {
  display: flex;
  gap: 2px;
  padding: var(--spacing-md) var(--spacing-xl) 0;
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
  background: var(--color-bg-surface);
}

.aligner-tab {
  padding: 10px var(--spacing-xl);
  font-size: var(--font-size-body);
  font-weight: 500;
  color: var(--color-text-muted);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  border-radius: var(--radius) var(--radius) 0 0;
  transition: all var(--transition-fast);
}

.aligner-tab:hover {
  color: var(--color-text);
  background: var(--color-bg-hover);
}

.aligner-tab--active {
  color: var(--color-primary);
  font-weight: 600;
  border-bottom-color: var(--color-primary);
}

.aligner-content {
  flex: 1;
  overflow-y: auto;
  display: flex;
  justify-content: center;
}

.aligner-content > * {
  width: var(--content-width);
  max-width: var(--content-max-width);
}
</style>
