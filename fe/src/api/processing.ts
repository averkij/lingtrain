import { apiFetch } from './client'

export interface ProcessingItem {
  id: number
  text_from: string
  text_to: string
  meta: Record<string, unknown>
}

export interface ProcessingResponse {
  items: ProcessingItem[]
  total: number
  page: number
  count: number
}

export interface MetaResponse {
  total_items: number
  lang_from: string
  lang_to: string
}

export interface IndexEntry {
  id: number
  index_id: number
  text_type: string
  text: string
}

export interface IndexResponse {
  index: IndexEntry[]
}

export interface EditParams {
  index_id: number
  text: string
  text_type: string
}

export interface SplitSentenceParams {
  index_id: number
  text_type: string
  position: number
}

export interface CandidateLine {
  id: number
  index_id: number
  text: string
}

export interface CandidatesResponse {
  candidates: CandidateLine[]
}

export interface ToggleExcludedParams {
  index_id: number
  text_type: string
  excluded: boolean
}

export function getProcessingPage(guid: string, count: number, page: number) {
  return apiFetch<ProcessingResponse>(
    `/api/aligner/processing/${guid}?count=${count}&page=${page}`,
  )
}

export function getProcessingMeta(guid: string) {
  return apiFetch<MetaResponse>(`/api/aligner/processing/${guid}/meta`)
}

export function getDocIndex(guid: string) {
  return apiFetch<IndexResponse>(`/api/aligner/processing/${guid}/index`)
}

export function editProcessing(guid: string, data: EditParams) {
  return apiFetch<void>(`/api/aligner/processing/${guid}/edit`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function splitSentence(guid: string, data: SplitSentenceParams) {
  return apiFetch<void>(`/api/aligner/processing/${guid}/split`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function getCandidates(
  guid: string,
  textType: string,
  indexId: number,
  countBefore: number,
  countAfter: number,
  shift: number,
) {
  const params = new URLSearchParams({
    text_type: textType,
    index_id: String(indexId),
    count_before: String(countBefore),
    count_after: String(countAfter),
    shift: String(shift),
  })
  return apiFetch<CandidatesResponse>(
    `/api/aligner/processing/${guid}/candidates?${params}`,
  )
}

export function toggleExcluded(guid: string, data: ToggleExcludedParams) {
  return apiFetch<void>(`/api/aligner/processing/${guid}/toggle-excluded`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}
