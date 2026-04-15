type TelegramWebApp = {
  ready: () => void
  expand: () => void
  initDataUnsafe?: {
    user?: {
      id?: number
      username?: string
      first_name?: string
      last_name?: string
    }
  }
}

declare global {
  interface Window {
    Telegram?: { WebApp?: TelegramWebApp }
  }
}

export function initTelegramWebApp(): number {
  const webApp = window.Telegram?.WebApp
  webApp?.ready()
  webApp?.expand()
  return webApp?.initDataUnsafe?.user?.id ?? 1
}
