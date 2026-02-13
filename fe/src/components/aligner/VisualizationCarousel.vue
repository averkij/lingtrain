<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { updateVisualization } from '@/api/alignments'

const { t } = useI18n()

const props = defineProps<{
  guid: string
  totalBatches: number
  userId: number
}>()

const currentBatch = ref(0)

const hasImages = computed(() => props.totalBatches > 0)

const imageUrl = computed(() => {
  if (!hasImages.value) return ''
  return `/static/img/${props.userId}/${props.guid}.best_${currentBatch.value}.png?t=${Date.now()}`
})

function prev() {
  if (currentBatch.value > 0) currentBatch.value--
}

function next() {
  if (currentBatch.value < props.totalBatches - 1) currentBatch.value++
}

async function refresh() {
  await updateVisualization(props.guid, {
    batch_ids: [currentBatch.value],
  })
  const old = currentBatch.value
  currentBatch.value = -1
  requestAnimationFrame(() => {
    currentBatch.value = old
  })
}

watch(
  () => props.totalBatches,
  (val) => {
    if (currentBatch.value >= val) currentBatch.value = Math.max(0, val - 1)
  },
)
</script>

<template>
  <div class="visualization">
    <div class="visualization__header">
      <h3 class="visualization__title">{{ t('aligner.visualization') }}</h3>
      <button v-if="hasImages" class="visualization__refresh" @click="refresh">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M11 7a4 4 0 1 1-1.2-2.8M11 2v2.2H8.8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        {{ t('aligner.refresh') }}
      </button>
    </div>

    <div v-if="!hasImages" class="visualization__empty">
      <div class="visualization__empty-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="1.5" />
          <circle cx="8.5" cy="8.5" r="1.5" fill="currentColor" />
          <path d="M21 15l-5-5L5 21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
      {{ t('aligner.noBatches') }}
    </div>

    <template v-else>
      <div class="visualization__image-wrapper">
        <img :src="imageUrl" alt="Alignment visualization" class="visualization__image" />
      </div>

      <div class="visualization__nav">
        <button class="visualization__btn" :disabled="currentBatch <= 0" @click="prev">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M8 3L5 7l3 4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          {{ t('aligner.prev') }}
        </button>
        <span class="visualization__info">{{ currentBatch + 1 }} / {{ totalBatches }}</span>
        <button
          class="visualization__btn"
          :disabled="currentBatch >= totalBatches - 1"
          @click="next"
        >
          {{ t('aligner.next') }}
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M6 3l3 4-3 4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.visualization {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-xs);
}

.visualization__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-md);
}

.visualization__title {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-strong);
}

.visualization__refresh {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 5px var(--spacing-md);
  font-size: 12px;
  font-weight: 500;
  color: var(--color-primary);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.visualization__refresh:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.visualization__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 13px;
  color: var(--color-text-muted);
  padding: var(--spacing-2xl);
}

.visualization__empty-icon {
  color: var(--color-border-input);
}

.visualization__image-wrapper {
  margin-bottom: var(--spacing-md);
  text-align: center;
}

.visualization__image {
  max-width: 200px;
  border-radius: var(--radius);
  border: 1px solid var(--color-border);
}

.visualization__nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
}

.visualization__btn {
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 5px var(--spacing-md);
  font-size: 12px;
  font-weight: 500;
  color: var(--color-primary);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.visualization__btn:hover:not(:disabled) {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.visualization__btn:disabled {
  color: var(--color-text-muted);
  cursor: default;
  opacity: 0.5;
}

.visualization__info {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  min-width: 60px;
  text-align: center;
  font-variant-numeric: tabular-nums;
}
</style>
