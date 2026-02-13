<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="handbook-page">
    <h1 class="handbook-title">{{ t('apps.handbookTitle') }}</h1>
  </div>
</template>

<style scoped>
.handbook-page {
  max-width: 720px;
  margin: 0 auto;
  padding: var(--spacing-2xl) var(--spacing-xl);
}

.handbook-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text-strong);
}
</style>
