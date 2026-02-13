<script setup lang="ts">
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAlignerStore } from '@/stores/aligner'
import { listDocuments, type DocumentOut } from '@/api/documents'
import LanguagePairSelector from '@/components/aligner/LanguagePairSelector.vue'
import DocumentUploadPanel from '@/components/aligner/DocumentUploadPanel.vue'
import SplittedPreview from '@/components/aligner/SplittedPreview.vue'
import MarksPanel from '@/components/aligner/MarksPanel.vue'

const { t } = useI18n()
const aligner = useAlignerStore()

if (!aligner.langFrom) aligner.langFrom = 'en'
if (!aligner.langTo) aligner.langTo = 'ru'

const docsFrom = ref<DocumentOut[]>([])
const docsTo = ref<DocumentOut[]>([])
const selectedFromGuid = ref<string | null>(null)
const selectedToGuid = ref<string | null>(null)

async function loadDocsFrom() {
  docsFrom.value = await listDocuments(aligner.langFrom)
  if (docsFrom.value.length > 0 && !selectedFromGuid.value) {
    selectedFromGuid.value = docsFrom.value[0]!.guid
  }
}

async function loadDocsTo() {
  docsTo.value = await listDocuments(aligner.langTo)
  if (docsTo.value.length > 0 && !selectedToGuid.value) {
    selectedToGuid.value = docsTo.value[0]!.guid
  }
}

watch(() => aligner.langFrom, () => {
  selectedFromGuid.value = null
  loadDocsFrom()
}, { immediate: true })
watch(() => aligner.langTo, () => {
  selectedToGuid.value = null
  loadDocsTo()
}, { immediate: true })

function selectDocFrom(doc: DocumentOut) {
  selectedFromGuid.value = doc.guid
}

function selectDocTo(doc: DocumentOut) {
  selectedToGuid.value = doc.guid
}

async function handleChangedFrom() {
  await loadDocsFrom()
}

async function handleChangedTo() {
  await loadDocsTo()
}
</script>

<template>
  <div class="aligner-documents">
    <div class="aligner-documents__header">
      <h1>{{ t('aligner.documents') }}</h1>
      <p class="aligner-documents__subtitle">{{ t('aligner.documentsSubtitle') }}</p>
    </div>

    <LanguagePairSelector v-model:lang-from="aligner.langFrom" v-model:lang-to="aligner.langTo" />

    <!-- Documents: two columns -->
    <div class="aligner-documents__section-title">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M4 1h6l3 3v10a1.5 1.5 0 0 1-1.5 1.5h-7A1.5 1.5 0 0 1 3 14V2.5A1.5 1.5 0 0 1 4 1Z" stroke="currentColor" stroke-width="1.2" />
        <path d="M10 1v3h3" stroke="currentColor" stroke-width="1.2" />
      </svg>
      {{ t('aligner.documents') }}
    </div>
    <div class="aligner-documents__row">
      <DocumentUploadPanel
        :lang="aligner.langFrom"
        :documents="docsFrom"
        :selected-guid="selectedFromGuid"
        @select="selectDocFrom"
        @changed="handleChangedFrom"
      />
      <DocumentUploadPanel
        :lang="aligner.langTo"
        :documents="docsTo"
        :selected-guid="selectedToGuid"
        @select="selectDocTo"
        @changed="handleChangedTo"
      />
    </div>

    <!-- Preview: two columns -->
    <div class="aligner-documents__section-title">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <rect x="2" y="2" width="12" height="12" rx="2" stroke="currentColor" stroke-width="1.2" />
        <path d="M5 5.5h6M5 8h6M5 10.5h4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
      </svg>
      {{ t('aligner.splittedPreview') }}
    </div>
    <p class="aligner-documents__info">
      {{ t('aligner.splittedInfo') }}
    </p>
    <div class="aligner-documents__row">
      <SplittedPreview :guid="selectedFromGuid" />
      <SplittedPreview :guid="selectedToGuid" />
    </div>

    <!-- Marks: two columns -->
    <div class="aligner-documents__section-title">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M3 3h4l1 2h5v8H3V3Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round" />
        <path d="M6 8h4M6 10.5h2.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
      </svg>
      {{ t('aligner.marks') }}
    </div>
    <p class="aligner-documents__info">
      {{ t('aligner.marksInfo') }}
    </p>
    <MarksPanel :guid-from="selectedFromGuid" :guid-to="selectedToGuid" />
  </div>
</template>

<style scoped>
.aligner-documents {
  padding: var(--spacing-xl) 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.aligner-documents__header {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

h1 {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-strong);
  margin: 0;
  letter-spacing: -0.3px;
}

.aligner-documents__subtitle {
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
}

.aligner-documents__section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-strong);
  margin-top: var(--spacing-md);
}

.aligner-documents__section-title svg {
  color: var(--color-primary);
}

.aligner-documents__info {
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-info-subtle);
  border-radius: var(--radius);
  border-left: 3px solid var(--color-primary);
}

.aligner-documents__row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  align-items: start;
}
</style>
