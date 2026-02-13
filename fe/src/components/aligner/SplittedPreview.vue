<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { getSplitted, downloadSplitted, type SplittedLine } from '@/api/documents'
import Pagination from './Pagination.vue'

const { t } = useI18n()

const props = defineProps<{
  guid: string | null
}>()

const lines = ref<SplittedLine[]>([])
const currentPage = ref(1)
const totalLines = ref(0)
const loading = ref(false)
const pageSize = 20

const totalPages = computed(() => Math.ceil(totalLines.value / pageSize))

async function fetchPage(page: number) {
  if (!props.guid) return
  loading.value = true
  try {
    const res = await getSplitted(props.guid, pageSize, page)
    lines.value = res.lines
    currentPage.value = res.page
    totalLines.value = res.total
  } finally {
    loading.value = false
  }
}

async function handleDownload() {
  if (!props.guid) return
  const blob = await downloadSplitted(props.guid)
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${props.guid}_splitted.txt`
  a.click()
  URL.revokeObjectURL(url)
}

watch(
  () => props.guid,
  (guid) => {
    if (guid) {
      currentPage.value = 1
      fetchPage(1)
    } else {
      lines.value = []
      totalLines.value = 0
    }
  },
  { immediate: true },
)
</script>

<template>
  <div class="splitted-preview">
    <div v-if="!guid" class="splitted-preview__empty">
      <div class="splitted-preview__empty-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M9 12h6M12 9v6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          <rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="1.5" />
        </svg>
      </div>
      <span>{{ t('aligner.selectDocument') }}</span>
    </div>

    <template v-else>
      <div class="splitted-preview__header">
        <span class="splitted-preview__line-count">{{ totalLines.toLocaleString() }} lines</span>
        <button class="splitted-preview__download" @click="handleDownload">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 2v7M4 6.5L7 9.5l3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M2 11h10" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
          </svg>
          {{ t('aligner.download') }}
        </button>
      </div>

      <div v-if="loading" class="splitted-preview__loading">
        <span class="splitted-preview__spinner" />
        {{ t('aligner.loading') }}
      </div>

      <div v-else class="splitted-preview__lines">
        <div v-for="line in lines" :key="line.id" class="splitted-preview__line">
          <span class="splitted-preview__line-num">{{ line.id }}</span>
          <span class="splitted-preview__line-text">
            {{ line.text }}
            <span v-if="line.mark" class="splitted-preview__mark">{{ line.mark }}</span>
          </span>
        </div>
      </div>

      <Pagination
        v-if="totalPages > 1"
        :current-page="currentPage"
        :total-pages="totalPages"
        @page-change="fetchPage"
      />
    </template>
  </div>
</template>

<style scoped>
.splitted-preview {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-xs);
}

.splitted-preview__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-2xl) var(--spacing-lg);
  color: var(--color-text-muted);
  font-size: 13px;
}

.splitted-preview__empty-icon {
  color: var(--color-border-input);
}

.splitted-preview__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-md);
}

.splitted-preview__line-count {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-muted);
}

.splitted-preview__download {
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

.splitted-preview__download:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.splitted-preview__loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: 13px;
  color: var(--color-text-muted);
  padding: var(--spacing-xl);
}

.splitted-preview__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.splitted-preview__lines {
  margin: 0 0 var(--spacing-md);
  font-size: 13px;
  line-height: 1.6;
  max-height: 520px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.splitted-preview__line {
  display: flex;
  gap: var(--spacing-sm);
  padding: 3px var(--spacing-sm);
  border-bottom: 1px solid var(--color-border);
}

.splitted-preview__line:last-child {
  border-bottom: none;
}

.splitted-preview__line-num {
  flex-shrink: 0;
  min-width: 32px;
  text-align: right;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
  padding-top: 1px;
}

.splitted-preview__line-text {
  flex: 1;
  color: var(--color-text);
  min-width: 0;
  word-break: break-word;
}

.splitted-preview__mark {
  display: inline-block;
  margin-left: var(--spacing-xs);
  padding: 0 6px;
  font-size: 10px;
  font-weight: 600;
  border-radius: 3px;
  background: var(--color-primary);
  color: #fff;
  vertical-align: middle;
  line-height: 18px;
}
</style>
