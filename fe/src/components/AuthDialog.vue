<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const mouseDownOnOverlay = ref(false)

function onOverlayMouseDown(e: MouseEvent) {
  mouseDownOnOverlay.value = e.target === e.currentTarget
}

function onOverlayMouseUp(e: MouseEvent) {
  if (mouseDownOnOverlay.value && e.target === e.currentTarget) {
    emit('close')
  }
  mouseDownOnOverlay.value = false
}
</script>

<template>
  <Teleport to="body">
    <Transition name="dialog">
      <div v-if="open" class="dialog-overlay" @mousedown="onOverlayMouseDown" @mouseup="onOverlayMouseUp">
        <div class="dialog-card">
          <button class="dialog-close" @click="emit('close')">&times;</button>
          <slot />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.dialog-card {
  position: relative;
  background: var(--color-bg-surface);
  border-radius: calc(var(--radius) * 2);
  padding: var(--spacing-xl);
  width: 400px;
  max-width: 90vw;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

.dialog-close {
  position: absolute;
  top: var(--spacing-md);
  right: var(--spacing-md);
  width: 28px;
  height: 28px;
  border: none;
  border-radius: var(--radius);
  background: transparent;
  color: var(--color-text-muted);
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color var(--transition-fast);
}

.dialog-close:hover {
  background: var(--color-bg-hover);
}

.dialog-enter-active,
.dialog-leave-active {
  transition: opacity 0.2s ease;
}

.dialog-enter-from,
.dialog-leave-to {
  opacity: 0;
}

.dialog-enter-active .dialog-card,
.dialog-leave-active .dialog-card {
  transition: transform 0.2s ease;
}

.dialog-enter-from .dialog-card {
  transform: scale(0.95);
}

.dialog-leave-to .dialog-card {
  transform: scale(0.95);
}
</style>
