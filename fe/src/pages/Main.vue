<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const appStore = useAppStore()
const authStore = useAuthStore()

const alignerActive = computed(() => route.path.startsWith('/aligner'))
const handbookActive = computed(() => route.path.startsWith('/handbook'))

const menuOpen = ref(false)
const menuPosition = ref({ left: '0px', bottom: '0px' })
const userBtnRef = ref<HTMLElement | null>(null)

function toggleMenu() {
  if (!menuOpen.value && userBtnRef.value) {
    const rect = userBtnRef.value.getBoundingClientRect()
    menuPosition.value = {
      left: `${rect.left}px`,
      bottom: `${window.innerHeight - rect.top + 4}px`,
    }
  }
  menuOpen.value = !menuOpen.value
}

function closeMenu() {
  menuOpen.value = false
}

function handleLogout() {
  closeMenu()
  authStore.logout()
  router.push({ name: 'landing' })
}
</script>

<template>
  <div class="main-layout" @click="closeMenu">
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
      <nav class="sidebar-nav">
        <RouterLink
          :to="{ name: 'aligner-documents' }"
          class="nav-item"
          :class="{ 'nav-item--active': alignerActive }"
        >
          <svg class="nav-icon" width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 2L28.124 9V23L16 30L3.876 23V9L16 2Z" fill="#dc2626" />
            <text x="16" y="21" text-anchor="middle" fill="white" font-size="15" font-weight="600" font-family="sans-serif">A</text>
          </svg>
          <span class="nav-label">{{ t('sidebar.aligner') }}</span>
        </RouterLink>
        <RouterLink
          :to="{ name: 'handbook' }"
          class="nav-item"
          :class="{ 'nav-item--active': handbookActive }"
        >
          <svg class="nav-icon" width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 2L28.124 9V23L16 30L3.876 23V9L16 2Z" fill="#2563eb" />
            <text x="16" y="21" text-anchor="middle" fill="white" font-size="15" font-weight="600" font-family="sans-serif">C</text>
          </svg>
          <span class="nav-label">{{ t('sidebar.handbook') }}</span>
        </RouterLink>
      </nav>

      <!-- User section -->
      <div class="sidebar-user">
        <button ref="userBtnRef" class="user-btn" @click.stop="toggleMenu">
          <svg class="user-avatar" width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 2L28.124 9V23L16 30L3.876 23V9L16 2Z" fill="#16a34a" />
            <text x="16" y="20.5" text-anchor="middle" fill="white" font-size="14" font-weight="600" font-family="sans-serif">L</text>
          </svg>
          <span class="user-name">{{ authStore.user?.username }}</span>
        </button>
      </div>
    </aside>

    <Teleport to="body">
      <Transition name="lt-user-menu">
        <div
          v-if="menuOpen"
          class="lt-user-menu"
          :style="{ position: 'fixed', left: menuPosition.left, bottom: menuPosition.bottom }"
          @click.stop
        >
          <button class="lt-user-menu__item" @click="closeMenu">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.8"/>
              <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
            {{ t('sidebar.settings') }}
          </button>
          <button class="lt-user-menu__item" @click="closeMenu">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.8"/>
              <path d="M9 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="12" cy="17" r="0.5" fill="currentColor" stroke="currentColor" stroke-width="1"/>
            </svg>
            {{ t('sidebar.help') }}
          </button>
          <div class="lt-user-menu__divider" />
          <button class="lt-user-menu__item lt-user-menu__item--danger" @click="handleLogout">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="16 17 21 12 16 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="21" y1="12" x2="9" y2="12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
            {{ t('sidebar.logOut') }}
          </button>
        </div>
      </Transition>
    </Teleport>

    <div class="main-content">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-width);
  height: 100vh;
  background: var(--color-bg-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  transition: width var(--transition-normal);
  overflow: hidden;
  flex-shrink: 0;
  z-index: 100;
}

.sidebar.collapsed {
  width: var(--sidebar-width-collapsed);
}

.sidebar.collapsed ~ .main-content {
  margin-left: var(--sidebar-width-collapsed);
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
  padding: var(--spacing-sm);
}

.main-content {
  flex: 1;
  margin-left: var(--sidebar-width);
  background: var(--color-bg);
  overflow-y: auto;
  transition: margin-left var(--transition-normal);
}

/* Nav items */
.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs);
  border: none;
  border-radius: var(--radius);
  background: transparent;
  text-decoration: none;
  cursor: pointer;
  transition: background-color var(--transition-fast);
  overflow: hidden;
  margin-bottom: 8px;
}

.nav-item:hover {
  background: var(--color-bg-hover);
}

.nav-item--active {
  background: var(--color-bg-hover);
}

.nav-icon {
  flex-shrink: 0;
}

.nav-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-subtle);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* User section */
.sidebar-user {
  flex-shrink: 0;
  border-top: 1px solid var(--color-border);
  padding: var(--spacing-sm);
}

.user-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  width: 100%;
  padding: 0;
  border: none;
  border-radius: var(--radius);
  background: transparent;
  cursor: pointer;
  transition: background-color var(--transition-fast);
  overflow: hidden;
}

.user-btn:hover {
  background: var(--color-bg-hover);
}

.user-avatar {
  flex-shrink: 0;
}

.user-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-subtle);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

<style>
/* Teleported menu — namespaced to avoid global collisions */
.lt-user-menu {
  width: 180px;
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: var(--spacing-xs) 0;
  z-index: 200;
}

.lt-user-menu__item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  background: transparent;
  color: var(--color-text-subtle);
  font-size: 13px;
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.lt-user-menu__item:hover {
  background: var(--color-bg-hover);
}

.lt-user-menu__item--danger {
  color: var(--color-error);
}

.lt-user-menu__divider {
  height: 1px;
  margin: var(--spacing-xs) 0;
  background: var(--color-border);
}

.lt-user-menu-enter-active,
.lt-user-menu-leave-active {
  transition:
    opacity var(--transition-fast),
    transform var(--transition-fast);
}

.lt-user-menu-enter-from,
.lt-user-menu-leave-to {
  opacity: 0;
  transform: translateY(4px);
}
</style>
