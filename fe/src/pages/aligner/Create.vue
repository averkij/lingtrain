<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAlignerStore } from '@/stores/aligner'
import { useEditorStore } from '@/stores/editor'
import ExportSettings from '@/components/aligner/ExportSettings.vue'
import BookPreview from '@/components/aligner/BookPreview.vue'
import DownloadPanel from '@/components/aligner/DownloadPanel.vue'

const { t } = useI18n()
const aligner = useAlignerStore()
const editor = useEditorStore()

const selectedGuid = ref('')
const format = ref('tmx')
const theme = ref('default')

onMounted(() => {
  aligner.fetchAlignments()
})

async function handlePreview() {
  if (!selectedGuid.value) return
  await editor.fetchBookPreview(selectedGuid.value, {
    format: format.value,
    theme: theme.value !== 'none' ? theme.value : undefined,
  })
}
</script>

<template>
  <div class="aligner-create">
    <h1>{{ t('aligner.create') }}</h1>

    <div class="aligner-create__alignment-select">
      <label class="aligner-create__label">{{ t('aligner.alignments') }}</label>
      <select v-model="selectedGuid" class="aligner-create__select">
        <option value="" disabled>--</option>
        <option v-for="a in aligner.alignments" :key="a.guid" :value="a.guid">
          {{ a.name }} ({{ a.lang_from }} &rarr; {{ a.lang_to }})
        </option>
      </select>
    </div>

    <template v-if="selectedGuid">
      <div class="aligner-create__panels">
        <ExportSettings v-model:format="format" v-model:theme="theme" />
        <DownloadPanel :guid="selectedGuid" :format="format" :theme="theme" />
      </div>

      <BookPreview :html="editor.bookPreview" @refresh="handlePreview" />
    </template>
  </div>
</template>

<style scoped>
.aligner-create {
  padding: var(--spacing-xl) var(--spacing-2xl);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
  max-width: 1200px;
}

h1 {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-strong);
  margin: 0;
  letter-spacing: -0.3px;
}

.aligner-create__alignment-select {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  max-width: 400px;
}

.aligner-create__label {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.aligner-create__select {
  padding: 8px var(--spacing-md);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius);
  cursor: pointer;
  transition: border-color var(--transition-fast);
}

.aligner-create__select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.aligner-create__panels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  align-items: start;
}
</style>
