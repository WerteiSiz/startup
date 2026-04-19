const API_BASE_URL = String(import.meta.env.VITE_API_BASE_URL || '').trim()

function buildUrl(path, query) {
  const safePath = path.startsWith('/') ? path : `/${path}`
  const url = new URL(`${API_BASE_URL}${safePath}`, window.location.origin)
  if (query && typeof query === 'object') {
    Object.entries(query).forEach(([key, value]) => {
      if (value === undefined || value === null || value === '') return
      url.searchParams.set(key, String(value))
    })
  }
  return url.toString()
}

async function parseError(response) {
  try {
    const data = await response.json()
    return data?.detail || data?.error || data?.message || `HTTP ${response.status}`
  } catch {
    return `HTTP ${response.status}`
  }
}

export async function apiRequest(path, options = {}) {
  const { query, headers, ...rest } = options
  const response = await fetch(buildUrl(path, query), {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(headers || {}),
    },
    ...rest,
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  if (response.status === 204) return null
  const text = await response.text()
  return text ? JSON.parse(text) : null
}
