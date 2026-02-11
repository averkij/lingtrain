<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import { ApiError } from '@/api/client'

const emit = defineEmits<{
  success: [email: string]
  'go-sign-in': []
}>()

const { t } = useI18n()
const authStore = useAuthStore()
const toast = useToast()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)

const canSubmit = computed(
  () =>
    username.value.length > 0 &&
    email.value.length > 0 &&
    password.value.length >= 6 &&
    confirmPassword.value.length > 0 &&
    !loading.value,
)

async function handleSubmit() {
  if (!canSubmit.value) return

  if (password.value !== confirmPassword.value) {
    toast.error(t('auth.passwordsDoNotMatch'))
    return
  }

  loading.value = true
  try {
    const res = await authStore.register(username.value, email.value, password.value)
    emit('success', res.email)
  } catch (e) {
    if (e instanceof ApiError) {
      toast.error(e.detail)
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-form">
    <h2 class="form-title">{{ t('auth.createAccount') }}</h2>

    <form @submit.prevent="handleSubmit">
      <label class="field-label">{{ t('auth.username') }}</label>
      <input v-model="username" type="text" class="field-input" autocomplete="username" />

      <label class="field-label">{{ t('auth.email') }}</label>
      <input v-model="email" type="email" class="field-input" autocomplete="email" />

      <label class="field-label">{{ t('auth.password') }}</label>
      <input v-model="password" type="password" class="field-input" autocomplete="new-password" />

      <label class="field-label">{{ t('auth.confirmPassword') }}</label>
      <input
        v-model="confirmPassword"
        type="password"
        class="field-input"
        autocomplete="new-password"
      />

      <button type="submit" class="submit-btn" :disabled="!canSubmit">
        {{ loading ? t('auth.registering') : t('auth.register') }}
      </button>
    </form>

    <p class="switch-text">
      {{ t('auth.hasAccount') }}
      <a href="#" @click.prevent="emit('go-sign-in')">{{ t('auth.signIn') }}</a>
    </p>
  </div>
</template>
