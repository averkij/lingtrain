import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import {
  apiLogin,
  apiRegister,
  apiVerifyEmail,
  apiResendVerification,
  apiGetMe,
  type UserOut,
} from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserOut | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(login: string, password: string) {
    const res = await apiLogin(login, password)
    token.value = res.access_token
    user.value = res.user
    localStorage.setItem('token', res.access_token)
  }

  async function register(username: string, email: string, password: string) {
    return apiRegister(username, email, password)
  }

  async function verifyEmail(email: string, code: string) {
    return apiVerifyEmail(email, code)
  }

  async function resendVerification(email: string) {
    return apiResendVerification(email)
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      user.value = await apiGetMe()
    } catch {
      logout()
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  return { user, token, isAuthenticated, isAdmin, login, register, verifyEmail, resendVerification, fetchUser, logout }
})
