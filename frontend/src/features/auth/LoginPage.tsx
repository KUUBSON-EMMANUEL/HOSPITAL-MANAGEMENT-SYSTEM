import * as React from "react"
import { useNavigate, useLocation } from "react-router-dom"
import { isAxiosError } from "axios"

import { useAuth } from "./AuthContext"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export function LoginPage() {
  const { login, verifyMfa } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as { from?: string } | null)?.from ?? "/"

  const [email, setEmail] = React.useState("")
  const [password, setPassword] = React.useState("")
  const [otpCode, setOtpCode] = React.useState("")
  const [challengeToken, setChallengeToken] = React.useState<string | null>(null)
  const [error, setError] = React.useState<string | null>(null)
  const [submitting, setSubmitting] = React.useState(false)

  async function handleLoginSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setSubmitting(true)
    try {
      const result = await login(email, password)
      if (result.mfaRequired) {
        setChallengeToken(result.challengeToken ?? null)
      } else {
        navigate(from, { replace: true })
      }
    } catch (err) {
      setError(extractError(err, "Invalid email or password."))
    } finally {
      setSubmitting(false)
    }
  }

  async function handleMfaSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!challengeToken) return
    setError(null)
    setSubmitting(true)
    try {
      await verifyMfa(challengeToken, otpCode)
      navigate(from, { replace: true })
    } catch (err) {
      setError(extractError(err, "Invalid verification code."))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-svh items-center justify-center bg-muted/30 p-4">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle>{challengeToken ? "Two-factor verification" : "Sign in"}</CardTitle>
          <CardDescription>
            {challengeToken
              ? "Enter the 6-digit code from your authenticator app."
              : "Hospital Management System"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {challengeToken ? (
            <form onSubmit={handleMfaSubmit} className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="otp">Verification code</Label>
                <Input
                  id="otp"
                  inputMode="numeric"
                  autoComplete="one-time-code"
                  maxLength={6}
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value)}
                  autoFocus
                  required
                />
              </div>
              {error && <p className="text-sm text-destructive">{error}</p>}
              <Button type="submit" disabled={submitting}>
                {submitting ? "Verifying…" : "Verify"}
              </Button>
            </form>
          ) : (
            <form onSubmit={handleLoginSubmit} className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  autoComplete="username"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoFocus
                  required
                />
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              {error && <p className="text-sm text-destructive">{error}</p>}
              <Button type="submit" disabled={submitting}>
                {submitting ? "Signing in…" : "Sign in"}
              </Button>
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

function extractError(err: unknown, fallback: string): string {
  if (isAxiosError(err)) {
    const data = err.response?.data as { error?: { message?: unknown }; detail?: unknown } | undefined
    const message = data?.error?.message ?? data?.detail
    if (typeof message === "string") return message
    if (message && typeof message === "object") return Object.values(message).flat().join(" ")
  }
  return fallback
}
