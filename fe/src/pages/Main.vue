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
  width: 240px;
  background: #fff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  transition: width 0.25s ease;
  overflow: hidden;
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: 48px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 48px;
  padding: 0 12px;
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
  border-radius: 6px;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  transition:
    background-color 0.15s,
    color 0.15s;
}

.sidebar-toggle:hover {
  background: #f3f4f6;
  color: #374151;
}

.toggle-icon {
  transition: transform 0.25s ease;
}

.toggle-icon.rotated {
  transform: rotate(180deg);
}

.sidebar-nav {
  flex: 1;
  padding: 8px;
}

.sidebar.collapsed .sidebar-nav {
  padding: 8px 4px;
}

.main-content {
  flex: 1;
  background: #fafafa;
}
</style>
