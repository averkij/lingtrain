<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useAppStore } from '@/stores/app'

const { t } = useI18n()
const appStore = useAppStore()
</script>

<template>
  <div class="main-layout">
    <aside class="sidebar" :class="{ collapsed: appStore.sidebarCollapsed }">
      <div class="sidebar-header">
        <button
          class="sidebar-toggle"
          :title="t('sidebar.collapse')"
          @click="appStore.toggleSidebar()"
        >
          <svg
            class="toggle-icon"
            :class="{ rotated: appStore.sidebarCollapsed }"
            width="18"
            height="18"
            viewBox="0 0 18 18"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M11.25 4.5L6.75 9L11.25 13.5"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
      </div>
      <nav class="sidebar-nav" />
    </aside>

    <div class="main-content" />
  </div>
</template>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: var(--sidebar-width);
  background: var(--color-bg-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  transition: width var(--transition-normal);
  overflow: hidden;
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: var(--sidebar-width-collapsed);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: var(--sidebar-width-collapsed);
  padding: 0 var(--spacing-md);
  flex-shrink: 0;
}

.sidebar.collapsed .sidebar-header {
  justify-content: center;
  padding: 0;
}

.sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: var(--radius);
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  transition:
    background-color var(--transition-fast),
    color var(--transition-fast);
}

.sidebar-toggle:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-subtle);
}

.toggle-icon {
  transition: transform var(--transition-normal);
}

.toggle-icon.rotated {
  transform: rotate(180deg);
}

.sidebar-nav {
  flex: 1;
  padding: var(--spacing-sm);
}

.sidebar.collapsed .sidebar-nav {
  padding: var(--spacing-sm) var(--spacing-xs);
}

.main-content {
  flex: 1;
  background: var(--color-bg);
}
</style>
