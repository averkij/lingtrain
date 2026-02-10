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
    },
    sidebar: {
      collapse: 'Collapse',
    },
  },
  ru: {
    landing: {
      title: 'Lingtrain',
      subtitle: 'Платформа языкового искусства',
      signIn: 'Войти',
    },
    sidebar: {
      collapse: 'Свернуть',
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
