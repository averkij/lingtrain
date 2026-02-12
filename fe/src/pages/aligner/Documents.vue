<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="aligner-documents">
    <h1>{{ t('aligner.documents') }}</h1>
  </div>
</template>

<style scoped>
.aligner-documents {
  padding: var(--spacing-xl);
}

h1 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-strong);
}
</style>
