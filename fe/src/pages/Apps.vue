<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const router = useRouter()
</script>

<template>
  <div class="apps-page">
    <h1 class="apps-title">{{ t('apps.welcome') }}</h1>

    <div class="apps-grid">
      <div class="app-card" @click="router.push({ name: 'aligner-documents' })">
        <div class="app-card__icon">
          <svg width="40" height="40" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 2L28.124 9V23L16 30L3.876 23V9L16 2Z" fill="#dc2626" />
            <text x="16" y="21" text-anchor="middle" fill="white" font-size="15" font-weight="600" font-family="sans-serif">A</text>
          </svg>
        </div>
        <div class="app-card__body">
          <h2 class="app-card__title">{{ t('apps.alignerTitle') }}</h2>
          <p class="app-card__desc">{{ t('apps.alignerDesc') }}</p>
        </div>
      </div>

      <div class="app-card" @click="router.push({ name: 'handbook' })">
        <div class="app-card__icon">
          <svg width="40" height="40" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 2L28.124 9V23L16 30L3.876 23V9L16 2Z" fill="#2563eb" />
            <text x="16" y="21" text-anchor="middle" fill="white" font-size="15" font-weight="600" font-family="sans-serif">C</text>
          </svg>
        </div>
        <div class="app-card__body">
          <h2 class="app-card__title">{{ t('apps.handbookTitle') }}</h2>
          <p class="app-card__desc">{{ t('apps.handbookDesc') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.apps-page {
  max-width: 720px;
  margin: 0 auto;
  padding: var(--spacing-2xl) var(--spacing-xl);
}

.apps-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text-strong);
  margin-bottom: var(--spacing-xl);
}

.apps-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.app-card {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-bg-surface);
  cursor: pointer;
  transition: box-shadow var(--transition-fast), border-color var(--transition-fast);
}

.app-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-xs);
}

.app-card__icon {
  flex-shrink: 0;
}

.app-card__title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-strong);
  margin-bottom: var(--spacing-xs);
}

.app-card__desc {
  font-size: 13px;
  color: var(--color-text-muted);
  line-height: 1.5;
}
</style>
