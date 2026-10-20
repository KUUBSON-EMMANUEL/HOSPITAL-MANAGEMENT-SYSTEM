// The backend's /auth/login/ returns tokens in the JSON body (not httpOnly
// cookies), so localStorage is the only place to persist them client-side.
// TODO: if XSS exposure becomes a real concern, move to an httpOnly-cookie
// refresh flow on the backend instead.
const ACCESS_KEY = "hms.access"
const REFRESH_KEY = "hms.refresh"

export const authTokens = {
  getAccess: () => localStorage.getItem(ACCESS_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_KEY),
  set: (access: string, refresh: string) => {
    localStorage.setItem(ACCESS_KEY, access)
    localStorage.setItem(REFRESH_KEY, refresh)
  },
  setAccess: (access: string) => localStorage.setItem(ACCESS_KEY, access),
  clear: () => {
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
  },
}
