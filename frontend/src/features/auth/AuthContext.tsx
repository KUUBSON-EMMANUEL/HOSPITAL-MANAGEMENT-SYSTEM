import * as React from "react"
import { useQuery, useQueryClient } from "@tanstack/react-query"

import { authApi } from "@/api/auth"
import { authTokens } from "@/lib/auth-tokens"
import { registerHardLogoutHandler } from "@/lib/api-client"
import type { UserProfile } from "@/types/api"

interface AuthContextValue {
  user: UserProfile | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<{ mfaRequired: boolean; challengeToken?: string }>
  verifyMfa: (challengeToken: string, otpCode: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = React.createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const queryClient = useQueryClient()
  const [hasSession, setHasSession] = React.useState(() => !!authTokens.getAccess())

  const meQuery = useQuery({
    queryKey: ["auth", "me"],
    queryFn: authApi.me,
    enabled: hasSession,
    retry: false,
    staleTime: 5 * 60 * 1000,
  })

  const clearSession = React.useCallback(() => {
    authTokens.clear()
    setHasSession(false)
    queryClient.setQueryData(["auth", "me"], null)
    queryClient.clear()
  }, [queryClient])

  React.useEffect(() => {
    registerHardLogoutHandler(clearSession)
  }, [clearSession])

  const login = React.useCallback(async (email: string, password: string) => {
    const result = await authApi.login(email, password)
    if (result.mfa_required) {
      return { mfaRequired: true, challengeToken: result.challenge_token }
    }
    authTokens.set(result.access!, result.refresh!)
    setHasSession(true)
    await queryClient.invalidateQueries({ queryKey: ["auth", "me"] })
    return { mfaRequired: false }
  }, [queryClient])

  const verifyMfa = React.useCallback(async (challengeToken: string, otpCode: string) => {
    const result = await authApi.verifyMfa(challengeToken, otpCode)
    authTokens.set(result.access, result.refresh)
    setHasSession(true)
    await queryClient.invalidateQueries({ queryKey: ["auth", "me"] })
  }, [queryClient])

  const logout = React.useCallback(async () => {
    const refresh = authTokens.getRefresh()
    try {
      if (refresh) await authApi.logout(refresh)
    } catch {
      // best-effort; clear local session regardless
    }
    clearSession()
  }, [clearSession])

  const value = React.useMemo<AuthContextValue>(
    () => ({
      user: meQuery.data ?? null,
      isLoading: hasSession && meQuery.isPending,
      login,
      verifyMfa,
      logout,
    }),
    [meQuery.data, meQuery.isPending, hasSession, login, verifyMfa, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = React.useContext(AuthContext)
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider")
  return ctx
}
