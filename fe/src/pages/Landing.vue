<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import AuthDialog from '@/components/AuthDialog.vue'
import SignInForm from '@/components/SignInForm.vue'
import RegisterForm from '@/components/RegisterForm.vue'
import VerifyEmailForm from '@/components/VerifyEmailForm.vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()
const toast = useToast()

const dialogOpen = ref(false)
const authView = ref<'sign-in' | 'register' | 'verify'>('sign-in')
const verifyEmail = ref('')

function openSignIn() {
  authView.value = 'sign-in'
  dialogOpen.value = true
}

function onLoginSuccess() {
  dialogOpen.value = false
  router.push({ name: 'main' })
}

function onRegisterSuccess(email: string) {
  verifyEmail.value = email
  authView.value = 'verify'
}

async function onGoVerify(email: string) {
  verifyEmail.value = email
  authView.value = 'verify'
  try {
    await authStore.resendVerification(email)
    toast.info(t('auth.codeSentTo', { email }))
  } catch {
    toast.error(t('auth.resendFailed'))
  }
}

function onVerifySuccess() {
  authView.value = 'sign-in'
}

function handleLogout() {
  authStore.logout()
}
</script>

<template>
  <div class="landing">
    <header class="topbar">
      <div class="topbar-left" />
      <div class="topbar-right">
        <LanguageSwitcher />
        <template v-if="authStore.isAuthenticated">
          <span class="user-name">{{ authStore.user?.username }}</span>
          <button class="sign-in-btn" @click="handleLogout">{{ t('landing.logout') }}</button>
        </template>
        <button v-else class="sign-in-btn" @click="openSignIn">{{ t('landing.signIn') }}</button>
      </div>
    </header>

    <main class="hero">
      <h1 class="hero-title">{{ t('landing.title') }}</h1>
      <p class="hero-subtitle">{{ t('landing.subtitle') }}</p>
    </main>

    <AuthDialog :open="dialogOpen" @close="dialogOpen = false">
      <SignInForm
        v-if="authView === 'sign-in'"
        @success="onLoginSuccess"
        @go-register="authView = 'register'"
        @go-verify="onGoVerify"
      />
      <RegisterForm
        v-else-if="authView === 'register'"
        @success="onRegisterSuccess"
        @go-sign-in="authView = 'sign-in'"
      />
      <VerifyEmailForm
        v-else-if="authView === 'verify'"
        :email="verifyEmail"
        @success="onVerifySuccess"
      />
    </AuthDialog>
  </div>
</template>

<style scoped>
.landing {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
}

.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--topbar-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-xl);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--color-border);
  z-index: 100;
}

.topbar-left {
  flex: 1;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-subtle);
}

.sign-in-btn {
  height: 32px;
  padding: 0 var(--spacing-lg);
  border: none;
  border-radius: var(--radius);
  background: var(--color-primary);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition:
    background-color var(--transition-fast),
    box-shadow var(--transition-fast);
}

.sign-in-btn:hover {
  background: var(--color-primary-hover);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

.hero {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--topbar-height) var(--spacing-xl) 0;
  text-align: center;
}

.hero-title {
  margin: -100px 0 0 0;
  font-size: 56px;
  font-weight: 700;
  color: var(--color-text-strong);
  letter-spacing: -1px;
}

.hero-subtitle {
  margin: var(--spacing-md) 0 0;
  font-size: 20px;
  font-weight: 400;
  color: var(--color-text-muted);
}
</style>
