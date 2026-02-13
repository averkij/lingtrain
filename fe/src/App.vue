<script setup lang="ts">
import ToastNotification from '@/components/ToastNotification.vue'
</script>

<template>
  <RouterView />
  <ToastNotification />
</template>

<style>
@import '@/assets/fonts.css';
@import '@/assets/variables.css';
@import '@/assets/forms.css';

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-family);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--color-text);
  background: var(--color-bg);
}
</style>
