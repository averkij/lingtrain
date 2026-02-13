import { apiFetch, apiUpload, apiDownload } from './client'

export interface DocumentOut {
  id: number
  guid: string
  lang: string
  name: string
  created_at: string
}

export interface SplittedLine {
  id: number
  text: string
  mark?: string | null
}

export interface SplittedResponse {
  lines: SplittedLine[]
  total: number
  page: number
  count: number
}

export interface Mark {
  text: string
  line: number
  type: string
}

export interface MarksResponse {
  marks: Mark[]
}

export function listDocuments(lang: string) {
  return apiFetch<DocumentOut[]>(`/api/aligner/documents/?lang=${encodeURIComponent(lang)}`)
}

export function uploadDocument(lang: string, file: File, cleanText = false) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('lang', lang)
  formData.append('clean_text', String(cleanText))
  return apiUpload<void>(`/api/aligner/documents/upload`, formData)
}

export function deleteDocument(guid: string) {
  return apiFetch<void>(`/api/aligner/documents/${guid}`, { method: 'DELETE' })
}

export function getSplitted(guid: string, count: number, page: number) {
  return apiFetch<SplittedResponse>(
    `/api/aligner/documents/${guid}/splitted?count=${count}&page=${page}`,
  )
}

export function downloadSplitted(guid: string) {
  return apiDownload(`/api/aligner/documents/${guid}/splitted/download`)
}

export function getDocumentMarks(guid: string) {
  return apiFetch<MarksResponse>(`/api/aligner/documents/${guid}/marks`)
}
