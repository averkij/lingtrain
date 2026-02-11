import { apiFetch } from './client'

export interface UserOut {
  id: number
  username: string
  email: string
  role: string
  is_active: boolean
  is_email_verified: boolean
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: UserOut
}

export function apiRegister(username: string, email: string, password: string) {
  return apiFetch<{ message: string; email: string }>('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify({ username, email, password }),
  })
}

export function apiLogin(login: string, password: string) {
  return apiFetch<TokenResponse>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ login, password }),
  })
}

export function apiVerifyEmail(email: string, code: string) {
  return apiFetch<{ message: string }>('/api/auth/verify-email', {
    method: 'POST',
    body: JSON.stringify({ email, code }),
  })
}

export function apiResendVerification(email: string) {
  return apiFetch<{ message: string; email: string }>('/api/auth/resend-verification', {
    method: 'POST',
    body: JSON.stringify({ email }),
  })
}

export function apiGetMe() {
  return apiFetch<UserOut>('/api/users/me')
}

export function apiGetUsers() {
  return apiFetch<UserOut[]>('/api/users')
}
