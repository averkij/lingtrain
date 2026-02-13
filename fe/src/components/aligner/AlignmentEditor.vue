<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useEditorStore } from '@/stores/editor'
import { useAlignerStore } from '@/stores/aligner'
import EditItem from './EditItem.vue'
import Pagination from './Pagination.vue'
import GoToPageDialog from './GoToPageDialog.vue'

const { t } = useI18n()
const editor = useEditorStore()
const aligner = useAlignerStore()

const props = defineProps<{
  guid: string
}>()

const pageSize = 20
const showGoToPage = ref(false)

async function loadPage(page: number) {
  await editor.fetchProcessingPage(props.guid, pageSize, page)
}

onMounted(() => {
  editor.fetchMeta(props.guid)
  loadPage(1)
})

watch(
  () => props.guid,
  () => {
    editor.fetchMeta(props.guid)
    loadPage(1)
  },
)

// Auto-refresh page count when alignment progress changes (e.g. new batches aligned)
watch(
  () => aligner.selectedAlignment?.curr_batches,
  () => {
    editor.fetchMeta(props.guid)
    // Refresh current page to pick up any changes
    editor.fetchProcessingPage(props.guid, pageSize, editor.currentPage)
  },
)

function handleGoToPage(page: number) {
  loadPage(page)
}
</script>

<template>
  <div class="alignment-editor">
    <div class="alignment-editor__header">
      <h3 class="alignment-editor__title">{{ t('aligner.editor') }}</h3>
      <button class="alignment-editor__goto" @click="showGoToPage = true">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M2 3h10M2 7h6M2 11h8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
        </svg>
        {{ t('aligner.goToPage') }}
      </button>
    </div>

    <Pagination
      v-if="editor.totalPages > 1"
      :current-page="editor.currentPage"
      :total-pages="editor.totalPages"
      @page-change="loadPage"
    />

    <div class="alignment-editor__content" :class="{ 'alignment-editor__content--loading': editor.loading }">
      <div v-if="editor.loading" class="alignment-editor__overlay">
        <span class="alignment-editor__spinner" />
      </div>
      <div class="alignment-editor__items">
        <EditItem
          v-for="item in editor.processing"
          :key="item.index_id"
          :item="item"
          :guid="guid"
          :page-size="pageSize"
        />
      </div>
    </div>

    <Pagination
      v-if="editor.totalPages > 1"
      :current-page="editor.currentPage"
      :total-pages="editor.totalPages"
      @page-change="loadPage"
    />

    <GoToPageDialog
      v-if="showGoToPage"
      :total-pages="editor.totalPages"
      @go="handleGoToPage"
      @close="showGoToPage = false"
    />
  </div>
</template>

<style scoped>
.alignment-editor {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.alignment-editor__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.alignment-editor__title {
  font-size: var(--font-size-section-title);
  font-weight: 700;
  color: var(--color-text-strong);
  letter-spacing: -0.2px;
}

.alignment-editor__goto {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 5px var(--spacing-md);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-primary);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.alignment-editor__goto:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.alignment-editor__content {
  position: relative;
  min-height: 100px;
}

.alignment-editor__content--loading .alignment-editor__items {
  opacity: 0.4;
  pointer-events: none;
  transition: opacity 0.15s ease;
}

.alignment-editor__overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.alignment-editor__spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.alignment-editor__items {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  transition: opacity 0.15s ease;
}
</style>
