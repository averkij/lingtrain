<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const tabs = [
  { name: 'aligner-documents', label: () => t('aligner.documents') },
  { name: 'aligner-alignments', label: () => t('aligner.alignments') },
  { name: 'aligner-create', label: () => t('aligner.create') },
]
</script>

<template>
  <div class="aligner-page">
    <nav class="aligner-tabs">
      <RouterLink
        v-for="tab in tabs"
        :key="tab.name"
        :to="{ name: tab.name }"
        class="aligner-tab"
        active-class="aligner-tab--active"
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
  gap: var(--spacing-xs);
  padding: var(--spacing-md) var(--spacing-xl) 0;
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.aligner-tab {
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-muted);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition:
    color var(--transition-fast),
    border-color var(--transition-fast);
}

.aligner-tab:hover {
  color: var(--color-text-subtle);
}

.aligner-tab--active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.aligner-content {
  flex: 1;
  overflow-y: auto;
}
</style>
