<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useEditorStore } from '@/stores/editor'
import EditItem from './EditItem.vue'
import Pagination from './Pagination.vue'
import GoToPageDialog from './GoToPageDialog.vue'

const { t } = useI18n()
const editor = useEditorStore()

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

    <div v-if="editor.loading" class="alignment-editor__loading">
      <span class="alignment-editor__spinner" />
      {{ t('aligner.loading') }}
    </div>

    <div v-else class="alignment-editor__items">
      <EditItem
        v-for="item in editor.processing"
        :key="item.id"
        :item="item"
        :guid="guid"
        :page-size="pageSize"
      />
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
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-strong);
  letter-spacing: -0.2px;
}

.alignment-editor__goto {
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

.alignment-editor__goto:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-hover);
}

.alignment-editor__loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: 13px;
  color: var(--color-text-muted);
  padding: var(--spacing-2xl);
}

.alignment-editor__spinner {
  width: 16px;
  height: 16px;
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
}
</style>
