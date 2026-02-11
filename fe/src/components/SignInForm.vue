<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import { ApiError } from '@/api/client'

const emit = defineEmits<{
  success: []
  'go-register': []
  'go-verify': [email: string]
}>()

const { t } = useI18n()
const authStore = useAuthStore()
const toast = useToast()

const login = ref('')
const password = ref('')
const loading = ref(false)

const canSubmit = computed(() => login.value.length > 0 && password.value.length > 0 && !loading.value)

async function handleSubmit() {
  if (!canSubmit.value) return
  loading.value = true
  try {
    await authStore.login(login.value, password.value)
    emit('success')
  } catch (e) {
    if (e instanceof ApiError) {
      if (e.detail === 'Email not verified' && typeof e.data.email === 'string') {
        emit('go-verify', e.data.email)
        return
      }
      toast.error(e.detail)
    }
  } finally {
    loading.value = false
  }
}

function handleGoogle() {
  toast.info(t('auth.googleComingSoon'))
}
</script>

<template>
  <div class="sign-in-form">
    <h2 class="form-title">{{ t('auth.signIn') }}</h2>

    <button class="google-btn" @click="handleGoogle">
      <svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844a4.14 4.14 0 01-1.796 2.716v2.259h2.908c1.702-1.567 2.684-3.875 2.684-6.615z"
          fill="#4285F4"
        />
        <path
          d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 009 18z"
          fill="#34A853"
        />
        <path
          d="M3.964 10.71A5.41 5.41 0 013.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.997 8.997 0 000 9c0 1.452.348 2.827.957 4.042l3.007-2.332z"
          fill="#FBBC05"
        />
        <path
          d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 00.957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z"
          fill="#EA4335"
        />
      </svg>
      {{ t('auth.continueWithGoogle') }}
    </button>

    <div class="divider">
      <span>{{ t('auth.or') }}</span>
    </div>

    <form @submit.prevent="handleSubmit">
      <label class="field-label">{{ t('auth.emailOrUsername') }}</label>
      <input v-model="login" type="text" class="field-input" autocomplete="username" />

      <label class="field-label">{{ t('auth.password') }}</label>
      <input v-model="password" type="password" class="field-input" autocomplete="current-password" />

      <button type="submit" class="submit-btn" :disabled="!canSubmit">
        {{ loading ? t('auth.signingIn') : t('auth.signIn') }}
      </button>
    </form>

    <p class="switch-text">
      {{ t('auth.noAccount') }}
      <a href="#" @click.prevent="emit('go-register')">{{ t('auth.register') }}</a>
    </p>
  </div>
</template>

<style scoped>
.google-btn {
  width: 100%;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius);
  background: var(--color-bg-surface);
  color: var(--color-text);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast);
}

.google-btn:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.divider {
  display: flex;
  align-items: center;
  margin: var(--spacing-lg) 0;
  color: var(--color-text-muted);
  font-size: 13px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-border);
}

.divider span {
  padding: 0 var(--spacing-md);
}
</style>
