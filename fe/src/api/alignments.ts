import { apiFetch } from './client'

export const AlignmentState = {
  INIT: 0,
  IN_PROGRESS: 1,
  IN_PROGRESS_DONE: 2,
  DONE: 3,
  ERROR: 4,
} as const

export type AlignmentStateValue = (typeof AlignmentState)[keyof typeof AlignmentState]

export interface AlignmentOut {
  id: number
  guid: string
  name: string
  lang_from: string
  lang_to: string
  state: AlignmentStateValue
  curr_batches: number
  total_batches: number
  is_uploaded: boolean
  proxy_from_loaded: boolean
  proxy_to_loaded: boolean
  created_at: string
}

export interface AlignmentCreate {
  name: string
  document_from_guid: string
  document_to_guid: string
}

export interface AlignNextParams {
  batch_size: number
  batch_count: number
}

export interface ResolveConflictsParams {
  batch_id: number
  decisions: Record<string, string>
}

export interface VisualizationParams {
  batch_id: number
  type: string
}

export interface Conflict {
  id: number
  batch_id: number
  type: string
  data: Record<string, unknown>
}

export interface ConflictsResponse {
  conflicts: Conflict[]
}

export interface ConflictDetail {
  id: number
  batch_id: number
  type: string
  left: string[]
  right: string[]
  candidates: string[][]
  data: Record<string, unknown>
}

export function listAlignments() {
  return apiFetch<AlignmentOut[]>('/api/aligner/alignments/')
}

export function createAlignment(data: AlignmentCreate) {
  return apiFetch<AlignmentOut>('/api/aligner/alignments/', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function deleteAlignment(guid: string) {
  return apiFetch<void>(`/api/aligner/alignments/${guid}`, { method: 'DELETE' })
}

export function startAlignment(guid: string, data: AlignNextParams) {
  return apiFetch<void>(`/api/aligner/alignments/${guid}/start`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function alignNext(guid: string, data: AlignNextParams) {
  return apiFetch<void>(`/api/aligner/alignments/${guid}/align-next`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function stopAlignment(guid: string) {
  return apiFetch<void>(`/api/aligner/alignments/${guid}/stop`, { method: 'POST' })
}

export function resolveConflicts(guid: string, data: ResolveConflictsParams) {
  return apiFetch<void>(`/api/aligner/alignments/${guid}/resolve-conflicts`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function getConflicts(guid: string) {
  return apiFetch<ConflictsResponse>(`/api/aligner/alignments/${guid}/conflicts`)
}

export function getConflictDetail(guid: string, id: number) {
  return apiFetch<ConflictDetail>(`/api/aligner/alignments/${guid}/conflicts/${id}`)
}

export function updateVisualization(guid: string, data: VisualizationParams) {
  return apiFetch<void>(`/api/aligner/alignments/${guid}/visualization`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function getProgress(guid: string) {
  return apiFetch<AlignmentOut>(`/api/aligner/alignments/${guid}/progress`)
}
