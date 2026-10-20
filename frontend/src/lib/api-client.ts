import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios"

import { authTokens } from "./auth-tokens"

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1"

export const apiClient = axios.create({ baseURL: API_BASE_URL })

let onHardLogout: (() => void) | null = null
export function registerHardLogoutHandler(handler: () => void) {
  onHardLogout = handler
}

apiClient.interceptors.request.use((config) => {
  const access = authTokens.getAccess()
  if (access) {
    config.headers.Authorization = `Bearer ${access}`
  }
  return config
})

// Single in-flight refresh promise so concurrent 401s don't each fire their
// own /auth/refresh/ request.
let refreshPromise: Promise<string> | null = null

async function refreshAccessToken(): Promise<string> {
  const refresh = authTokens.getRefresh()
  if (!refresh) throw new Error("No refresh token available.")
  const { data } = await axios.post<{ access: string }>(`${API_BASE_URL}/auth/refresh/`, { refresh })
  authTokens.setAccess(data.access)
  return data.access
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as (InternalAxiosRequestConfig & { _retried?: boolean }) | undefined

    if (error.response?.status !== 401 || !original || original._retried || original.url?.includes("/auth/refresh/")) {
      throw error
    }

    original._retried = true
    try {
      refreshPromise ??= refreshAccessToken().finally(() => {
        refreshPromise = null
      })
      const access = await refreshPromise
      original.headers.Authorization = `Bearer ${access}`
      return apiClient(original)
    } catch {
      authTokens.clear()
      onHardLogout?.()
      throw error
    }
  },
)
