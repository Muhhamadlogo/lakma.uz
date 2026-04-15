import { useMemo } from 'react'
import { initTelegramWebApp } from '../telegram/webapp'

export function useTelegramUserId(): number {
  return useMemo(() => initTelegramWebApp(), [])
}
