import { createI18n } from 'vue-i18n'

export type Locale = 'en' | 'ru'

export interface Language {
  code: Locale
  label: string
}

export const languages: Language[] = [
  { code: 'en', label: 'EN' },
  { code: 'ru', label: 'RU' },
]

const messages = {
  en: {
    landing: {
      title: 'Lingtrain',
      subtitle: 'Language Art Platform',
      signIn: 'Sign in',
      logout: 'Logout',
    },
    sidebar: {
      collapse: 'Collapse',
      aligner: 'Aligner',
      settings: 'Settings',
      help: 'Help',
      logOut: 'Log out',
    },
    aligner: {
      title: 'Aligner',
      documents: 'Documents',
      alignments: 'Alignments',
      create: 'Create',
    },
    auth: {
      signIn: 'Sign in',
      signingIn: 'Signing in…',
      register: 'Register',
      registering: 'Registering…',
      createAccount: 'Create account',
      emailOrUsername: 'Email or username',
      username: 'Username',
      email: 'Email',
      password: 'Password',
      confirmPassword: 'Confirm password',
      continueWithGoogle: 'Continue with Google',
      or: 'or',
      noAccount: "Don't have an account?",
      hasAccount: 'Already have an account?',
      googleComingSoon: 'Google sign-in coming soon',
      passwordsDoNotMatch: 'Passwords do not match',
      passwordTooShort: 'Password must be at least 6 characters',
      usernameLatin: 'Only latin letters, digits, hyphens, and underscores',
      verifyEmail: 'Verify your email',
      codeSentTo: 'We sent a code to {email}',
      verificationCode: 'Verification code',
      codePlaceholder: '000000',
      verify: 'Verify',
      verifying: 'Verifying…',
      emailVerified: 'Email verified! You can now sign in.',
      resendFailed: 'Failed to resend verification code',
    },
    admin: {
      title: 'Admin Panel',
      usersTable: 'Users',
      colId: 'ID',
      colUsername: 'Username',
      colEmail: 'Email',
      colRole: 'Role',
      colVerified: 'Verified',
      colActive: 'Active',
      yes: 'Yes',
      no: 'No',
      loading: 'Loading…',
      loadError: 'Failed to load users',
    },
  },
  ru: {
    landing: {
      title: 'Lingtrain',
      subtitle: 'Платформа языкового искусства',
      signIn: 'Войти',
      logout: 'Выйти',
    },
    sidebar: {
      collapse: 'Свернуть',
      aligner: 'Выравниватель',
      settings: 'Настройки',
      help: 'Помощь',
      logOut: 'Выйти',
    },
    aligner: {
      title: 'Выравниватель',
      documents: 'Тексты',
      alignments: 'Выравнивания',
      create: 'Экспорт',
    },
    auth: {
      signIn: 'Войти',
      signingIn: 'Вход…',
      register: 'Регистрация',
      registering: 'Регистрация…',
      createAccount: 'Создать аккаунт',
      emailOrUsername: 'Email или имя пользователя',
      username: 'Имя пользователя',
      email: 'Email',
      password: 'Пароль',
      confirmPassword: 'Подтвердите пароль',
      continueWithGoogle: 'Продолжить с Google',
      or: 'или',
      noAccount: 'Нет аккаунта?',
      hasAccount: 'Уже есть аккаунт?',
      googleComingSoon: 'Вход через Google скоро появится',
      passwordsDoNotMatch: 'Пароли не совпадают',
      passwordTooShort: 'Пароль должен быть не менее 6 символов',
      usernameLatin: 'Только латинские буквы, цифры, дефисы и подчёркивания',
      verifyEmail: 'Подтвердите email',
      codeSentTo: 'Мы отправили код на {email}',
      verificationCode: 'Код подтверждения',
      codePlaceholder: '000000',
      verify: 'Подтвердить',
      verifying: 'Проверка…',
      emailVerified: 'Email подтверждён! Теперь вы можете войти.',
      resendFailed: 'Не удалось отправить код повторно',
    },
    admin: {
      title: 'Панель администратора',
      usersTable: 'Пользователи',
      colId: 'ID',
      colUsername: 'Имя пользователя',
      colEmail: 'Email',
      colRole: 'Роль',
      colVerified: 'Подтверждён',
      colActive: 'Активен',
      yes: 'Да',
      no: 'Нет',
      loading: 'Загрузка…',
      loadError: 'Не удалось загрузить пользователей',
    },
  },
}

const savedLocale = localStorage.getItem('locale') as Locale | null

const i18n = createI18n({
  legacy: false,
  locale: savedLocale ?? 'en',
  fallbackLocale: 'en',
  messages,
})

export default i18n
