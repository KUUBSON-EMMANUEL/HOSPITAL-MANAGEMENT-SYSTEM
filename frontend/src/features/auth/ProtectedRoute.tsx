import { Navigate, useLocation } from "react-router-dom"

import { useAuth } from "./AuthContext"
import { authTokens } from "@/lib/auth-tokens"

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth()
  const location = useLocation()

  if (!authTokens.getAccess()) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />
  }

  if (isLoading) {
    return (
      <div className="flex min-h-svh items-center justify-center text-sm text-muted-foreground">
        Loading…
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />
  }

  return children
}
