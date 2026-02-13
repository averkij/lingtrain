import { apiFetch, apiDownload } from './client'

export interface DownloadProcessingParams {
  format: string
}

export interface BookPreviewParams {
  format: string
  theme?: string
}

export interface PreviewResponse {
  html: string
}

export interface DownloadBookParams {
  format: string
  theme?: string
}

export function downloadProcessing(guid: string, data: DownloadProcessingParams) {
  const params = new URLSearchParams({ format: data.format })
  return apiDownload(`/api/aligner/export/${guid}/processing?${params}`)
}

export function getBookPreview(guid: string, data: BookPreviewParams) {
  const params = new URLSearchParams({ format: data.format })
  if (data.theme) params.set('theme', data.theme)
  return apiFetch<PreviewResponse>(`/api/aligner/export/${guid}/book/preview?${params}`)
}

export function downloadBook(guid: string, data: DownloadBookParams) {
  const params = new URLSearchParams({ format: data.format })
  if (data.theme) params.set('theme', data.theme)
  return apiDownload(`/api/aligner/export/${guid}/book?${params}`)
}
