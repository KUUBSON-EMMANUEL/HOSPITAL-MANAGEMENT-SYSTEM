import { apiClient } from "@/lib/api-client"
import type { UserProfile } from "@/types/api"

export interface LoginResult {
  mfa_required?: boolean
  challenge_token?: string
  access?: string
  refresh?: string
}

export const authApi = {
  login: (email: string, password: string) =>
    apiClient.post<LoginResult>("/auth/login/", { email, password }).then((r) => r.data),

  verifyMfa: (challenge_token: string, otp_code: string) =>
    apiClient
      .post<{ access: string; refresh: string }>("/auth/mfa/verify/", { challenge_token, otp_code })
      .then((r) => r.data),

  logout: (refresh: string) => apiClient.post("/auth/logout/", { refresh }),

  me: () => apiClient.get<UserProfile>("/auth/me/").then((r) => r.data),

  changePassword: (old_password: string, new_password: string) =>
    apiClient.post("/auth/change-password/", { old_password, new_password }),

  mfaEnable: () =>
    apiClient.post<{ secret: string; provisioning_uri: string }>("/auth/mfa/enable/").then((r) => r.data),

  mfaVerifySetup: (otp_code: string) => apiClient.post("/auth/mfa/verify-setup/", { otp_code }),

  mfaDisable: (password: string) => apiClient.post("/auth/mfa/disable/", { password }),
}
