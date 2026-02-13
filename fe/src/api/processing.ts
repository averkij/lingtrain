import { apiFetch } from './client'

export interface ProcessingItem {
  index_id: number
  batch_id: number
  batch_index_id: number
  text_from: string
  text_to: string
  line_id_from: string // JSON array string e.g. "[1,2]"
  line_id_to: string // JSON array string e.g. "[3,4]"
  processing_from_id: number
  processing_to_id: number
}

export interface ProcessingResponse {
  items: ProcessingItem[]
  meta: {
    page: number
    total_pages: number
  }
  proxy_from_dict: Record<string, unknown>
  proxy_to_dict: Record<string, unknown>
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
  operation: string
  batch_id: number
  batch_index_id: number
  target?: string
  candidate_line_id?: number
  candidate_text?: string
  line_id_from?: number
  line_id_to?: number
}

export interface SplitSentenceParams {
  direction: string
  line_id: number
  part1: string
  part2: string
}

export interface CandidateLine {
  id: number
  index_id: number
  text: string
}

export interface CandidatesResponse {
  items: CandidateLine[]
}

export function getProcessingPage(guid: string, count: number, page: number) {
  return apiFetch<ProcessingResponse>(
    `/api/aligner/processing/${guid}/page?count=${count}&page=${page}`,
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

export function switchExcluded(guid: string, lineId: number, textType: string) {
  const params = new URLSearchParams({
    line_id: String(lineId),
    text_type: textType,
  })
  return apiFetch<void>(`/api/aligner/processing/${guid}/exclude?${params}`, {
    method: 'POST',
  })
}
