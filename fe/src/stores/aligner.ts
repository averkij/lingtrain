import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  listDocuments,
  uploadDocument,
  deleteDocument as apiDeleteDocument,
  type DocumentOut,
} from '@/api/documents'
import {
  listAlignments,
  createAlignment as apiCreateAlignment,
  deleteAlignment as apiDeleteAlignment,
  startAlignment as apiStartAlignment,
  alignNext as apiAlignNext,
  stopAlignment as apiStopAlignment,
  resolveConflicts as apiResolveConflicts,
  getProgress,
  type AlignmentOut,
  type AlignmentCreate,
  type AlignNextParams,
  type ResolveConflictsParams,
} from '@/api/alignments'

export const useAlignerStore = defineStore('aligner', () => {
  const documents = ref<DocumentOut[]>([])
  const alignments = ref<AlignmentOut[]>([])
  const langFrom = ref<string>('')
  const langTo = ref<string>('')
  const selectedAlignment = ref<AlignmentOut | null>(null)
  const loading = ref(false)
  const polling = ref<number | null>(null)

  async function fetchDocuments(lang: string) {
    loading.value = true
    try {
      documents.value = await listDocuments(lang)
    } finally {
      loading.value = false
    }
  }

  async function doUploadDocument(lang: string, file: File, cleanText = false) {
    await uploadDocument(lang, file, cleanText)
    await fetchDocuments(lang)
  }

  async function deleteDocument(guid: string, lang: string) {
    await apiDeleteDocument(guid)
    await fetchDocuments(lang)
  }

  async function fetchAlignments() {
    loading.value = true
    try {
      alignments.value = await listAlignments()
    } finally {
      loading.value = false
    }
  }

  async function createAlignment(data: AlignmentCreate) {
    const result = await apiCreateAlignment(data)
    await fetchAlignments()
    return result
  }

  async function deleteAlignment(guid: string) {
    await apiDeleteAlignment(guid)
    await fetchAlignments()
  }

  async function startAlignment(guid: string, data: AlignNextParams) {
    await apiStartAlignment(guid, data)
    startPolling(guid)
  }

  async function alignNext(guid: string, data: AlignNextParams) {
    await apiAlignNext(guid, data)
    startPolling(guid)
  }

  async function stopAlignment(guid: string) {
    await apiStopAlignment(guid)
    stopPolling()
    const updated = await getProgress(guid)
    selectedAlignment.value = updated
  }

  async function resolveConflicts(guid: string, data: ResolveConflictsParams) {
    await apiResolveConflicts(guid, data)
  }

  function startPolling(guid: string) {
    stopPolling()
    polling.value = window.setInterval(async () => {
      try {
        const updated = await getProgress(guid)
        selectedAlignment.value = updated
        const idx = alignments.value.findIndex((a) => a.guid === guid)
        if (idx !== -1) alignments.value[idx] = updated
      } catch {
        stopPolling()
      }
    }, 5000)
  }

  function stopPolling() {
    if (polling.value !== null) {
      clearInterval(polling.value)
      polling.value = null
    }
  }

  return {
    documents,
    alignments,
    langFrom,
    langTo,
    selectedAlignment,
    loading,
    polling,
    fetchDocuments,
    uploadDocument: doUploadDocument,
    deleteDocument,
    fetchAlignments,
    createAlignment,
    deleteAlignment,
    startAlignment,
    alignNext,
    stopAlignment,
    resolveConflicts,
    startPolling,
    stopPolling,
  }
})
