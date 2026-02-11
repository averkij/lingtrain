<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import { ApiError } from '@/api/client'

const props = defineProps<{
  email: string
}>()

const emit = defineEmits<{
  success: []
}>()

const { t } = useI18n()
const authStore = useAuthStore()
const toast = useToast()

const code = ref('')
const loading = ref(false)

const canSubmit = computed(() => code.value.length === 6 && !loading.value)

async function handleSubmit() {
  if (!canSubmit.value) return
  loading.value = true
  try {
    await authStore.verifyEmail(props.email, code.value)
    toast.success(t('auth.emailVerified'))
    emit('success')
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
  <div class="verify-form">
    <h2 class="form-title">{{ t('auth.verifyEmail') }}</h2>
    <p class="form-hint">{{ t('auth.codeSentTo', { email: props.email }) }}</p>

    <form @submit.prevent="handleSubmit">
      <label class="field-label">{{ t('auth.verificationCode') }}</label>
      <input
        v-model="code"
        type="text"
        class="field-input code-input"
        maxlength="6"
        inputmode="numeric"
        autocomplete="one-time-code"
        :placeholder="t('auth.codePlaceholder')"
      />

      <button type="submit" class="submit-btn" :disabled="!canSubmit">
        {{ loading ? t('auth.verifying') : t('auth.verify') }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.code-input {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 8px;
  font-family: monospace;
  height: 48px;
}
</style>
