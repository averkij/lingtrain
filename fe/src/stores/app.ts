import { ref } from 'vue'
import { defineStore } from 'pinia'
import i18n, { type Locale, languages } from '@/i18n'

export const useAppStore = defineStore('app', () => {
  const locale = ref<Locale>(i18n.global.locale.value)
  const sidebarCollapsed = ref(false)

  function setLocale(code: Locale) {
    locale.value = code
    i18n.global.locale.value = code
    localStorage.setItem('locale', code)
  }

  function cycleLocale() {
    const currentIndex = languages.findIndex((l) => l.code === locale.value)
    const next = languages[(currentIndex + 1) % languages.length]!
    setLocale(next.code)
  }

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  return { locale, sidebarCollapsed, setLocale, cycleLocale, toggleSidebar }
})
