import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  getProcessingPage,
  getProcessingMeta,
  getDocIndex,
  editProcessing as apiEditProcessing,
  splitSentence as apiSplitSentence,
  getCandidates,
  switchExcluded as apiSwitchExcluded,
  type ProcessingItem,
  type MetaResponse,
  type IndexEntry,
  type EditParams,
  type SplitSentenceParams,
  type CandidateLine,
} from '@/api/processing'
import {
  getConflicts,
  getConflictDetail,
  type Conflict,
  type ConflictDetail,
} from '@/api/alignments'
import {
  downloadProcessing as apiDownloadProcessing,
  getBookPreview as apiGetBookPreview,
  downloadBook as apiDownloadBook,
  type DownloadProcessingParams,
  type BookPreviewParams,
  type DownloadBookParams,
} from '@/api/export'

export const useEditorStore = defineStore('editor', () => {
  const processing = ref<ProcessingItem[]>([])
  const processingMeta = ref<MetaResponse | null>(null)
  const docIndex = ref<IndexEntry[]>([])
  const conflicts = ref<Conflict[]>([])
  const conflictDetails = ref<ConflictDetail | null>(null)
  const candidates = ref<CandidateLine[]>([])
  const bookPreview = ref<string>('')
  const currentPage = ref(1)
  const totalPages = ref(0)
  const loading = ref(false)

  async function fetchProcessingPage(guid: string, count: number, page: number) {
    loading.value = true
    try {
      const res = await getProcessingPage(guid, count, page)
      processing.value = res.items
      currentPage.value = res.meta.page
      totalPages.value = res.meta.total_pages
    } finally {
      loading.value = false
    }
  }

  async function fetchMeta(guid: string) {
    processingMeta.value = await getProcessingMeta(guid)
  }

  async function fetchDocIndex(guid: string) {
    const res = await getDocIndex(guid)
    docIndex.value = res.index
  }

  async function editProcessing(guid: string, data: EditParams) {
    await apiEditProcessing(guid, data)
  }

  async function splitSentence(guid: string, data: SplitSentenceParams) {
    await apiSplitSentence(guid, data)
  }

  async function fetchCandidates(
    guid: string,
    textType: string,
    indexId: number,
    countBefore: number,
    countAfter: number,
    shift: number,
  ) {
    const res = await getCandidates(guid, textType, indexId, countBefore, countAfter, shift)
    candidates.value = res.items
  }

  async function fetchConflicts(guid: string) {
    const res = await getConflicts(guid)
    conflicts.value = res.conflicts
  }

  async function fetchConflictDetail(guid: string, id: number) {
    conflictDetails.value = await getConflictDetail(guid, id)
  }

  async function switchExcluded(guid: string, lineId: number, textType: string) {
    await apiSwitchExcluded(guid, lineId, textType)
  }

  async function fetchBookPreview(guid: string, data: BookPreviewParams) {
    const res = await apiGetBookPreview(guid, data)
    bookPreview.value = res.html
  }

  async function downloadBook(guid: string, data: DownloadBookParams) {
    return apiDownloadBook(guid, data)
  }

  async function downloadProcessing(guid: string, data: DownloadProcessingParams) {
    return apiDownloadProcessing(guid, data)
  }

  return {
    processing,
    processingMeta,
    docIndex,
    conflicts,
    conflictDetails,
    candidates,
    bookPreview,
    currentPage,
    totalPages,
    loading,
    fetchProcessingPage,
    fetchMeta,
    fetchDocIndex,
    editProcessing,
    splitSentence,
    fetchCandidates,
    fetchConflicts,
    fetchConflictDetail,
    switchExcluded,
    fetchBookPreview,
    downloadBook,
    downloadProcessing,
  }
})
