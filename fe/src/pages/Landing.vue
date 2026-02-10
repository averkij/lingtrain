<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'

const router = useRouter()
const { t } = useI18n()

function goToMain() {
  router.push({ name: 'main' })
}
</script>

<template>
  <div class="landing">
    <header class="topbar">
      <div class="topbar-left" />
      <div class="topbar-right">
        <LanguageSwitcher />
        <button class="sign-in-btn" @click="goToMain">{{ t('landing.signIn') }}</button>
      </div>
    </header>

    <main class="hero">
      <h1 class="hero-title">{{ t('landing.title') }}</h1>
      <p class="hero-subtitle">{{ t('landing.subtitle') }}</p>
    </main>
  </div>
</template>

<style scoped>
.landing {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #fafafa;
}

.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #e5e7eb;
  z-index: 100;
}

.topbar-left {
  flex: 1;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sign-in-btn {
  height: 32px;
  padding: 0 16px;
  border: none;
  border-radius: 6px;
  background: #2563eb;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition:
    background-color 0.15s,
    box-shadow 0.15s;
}

.sign-in-btn:hover {
  background: #1d4ed8;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

.hero {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 56px 24px 0;
  text-align: center;
}

.hero-title {
  margin: 0;
  font-size: 56px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -1px;
}

.hero-subtitle {
  margin: 12px 0 0;
  font-size: 20px;
  font-weight: 400;
  color: #6b7280;
}
</style>
