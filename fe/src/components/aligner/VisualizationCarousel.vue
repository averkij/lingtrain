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

const PAGE_SIZE = 5
const pageStart = ref(0)
const refreshKey = ref(0)
const loading = ref(false)

const hasImages = computed(() => props.totalBatches > 0)

const visibleBatches = computed(() => {
  const end = Math.min(pageStart.value + PAGE_SIZE, props.totalBatches)
  const batches: number[] = []
  for (let i = pageStart.value; i < end; i++) batches.push(i)
  return batches
})

const totalCarouselPages = computed(() => Math.ceil(props.totalBatches / PAGE_SIZE))
const currentCarouselPage = computed(() => Math.floor(pageStart.value / PAGE_SIZE) + 1)

function imageUrl(batch: number) {
  return `/static/img/${props.userId}/${props.guid}.best_${batch}.png?v=${refreshKey.value}`
}

function prev() {
  pageStart.value = Math.max(0, pageStart.value - PAGE_SIZE)
}

function next() {
  if (pageStart.value + PAGE_SIZE < props.totalBatches) {
    pageStart.value += PAGE_SIZE
  }
}

async function refresh() {
  loading.value = true
  try {
    await updateVisualization(props.guid, {
      batch_ids: visibleBatches.value,
    })
    refreshKey.value++
  } finally {
    loading.value = false
  }
}

watch(
  () => props.totalBatches,
  (val) => {
    if (pageStart.value >= val) pageStart.value = Math.max(0, val - PAGE_SIZE)
  },
)
</script>

<template>
  <div class="visualization">
    <div class="visualization__header">
      <h3 class="visualization__title">{{ t('aligner.visualization') }}</h3>
      <button v-if="hasImages" class="visualization__refresh" :disabled="loading" @click="refresh">
        <svg
          width="14" height="14" viewBox="0 0 14 14" fill="none"
          :class="{ 'visualization__refresh-icon--spinning': loading }"
        >
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
      <div class="visualization__content" :class="{ 'visualization__content--loading': loading }">
        <div class="visualization__grid">
          <div
            v-for="batch in visibleBatches"
            :key="batch"
            class="visualization__grid-item"
          >
            <div class="visualization__batch-label">{{ batch + 1 }}</div>
            <img :src="imageUrl(batch)" alt="Alignment visualization" class="visualization__image" />
          </div>
        </div>
      </div>

      <div v-if="totalCarouselPages > 1" class="visualization__nav">
        <button class="visualization__btn" :disabled="pageStart <= 0" @click="prev">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M8 3L5 7l3 4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          {{ t('aligner.prev') }}
        </button>
        <span class="visualization__info">{{ currentCarouselPage }} / {{ totalCarouselPages }}</span>
        <button
          class="visualization__btn"
          :disabled="pageStart + PAGE_SIZE >= totalBatches"
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

.visualization__refresh:hover:not(:disabled) {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.visualization__refresh:disabled {
  opacity: 0.6;
  cursor: default;
}

.visualization__refresh-icon--spinning {
  animation: spin 0.8s linear infinite;
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

.visualization__content {
  transition: opacity 0.15s ease;
  margin-bottom: var(--spacing-md);
}

.visualization__content--loading {
  opacity: 0.4;
  pointer-events: none;
}

.visualization__grid {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.visualization__grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  width: 180px;
}

.visualization__batch-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

.visualization__image {
  width: 180px;
  min-height: 200px;
  object-fit: contain;
  border-radius: var(--radius);
  border: 1px solid var(--color-border);
  background: var(--color-bg-hover);
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

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
