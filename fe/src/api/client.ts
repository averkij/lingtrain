const BASE_URL = ''

export class ApiError extends Error {
  public data: Record<string, unknown>

  constructor(
    public status: number,
    public detail: string,
    data: Record<string, unknown> = {},
  ) {
    super(detail)
    this.data = data
  }
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('token')

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...((options.headers as Record<string, string>) ?? {}),
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers,
  })

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new ApiError(res.status, body.detail ?? 'Unknown error', body)
  }

  return res.json() as Promise<T>
}
