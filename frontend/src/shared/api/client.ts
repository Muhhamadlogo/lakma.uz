import type { CartResponse, ChatResponse, Product } from '../types/api'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    ...init,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `Request failed: ${res.status}`)
  }
  if (res.status === 204) {
    return undefined as T
  }
  return (await res.json()) as T
}

export const api = {
  listProducts: (query?: string) => request<Product[]>(`/products${query ? `?query=${encodeURIComponent(query)}` : ''}`),
  getCart: (userId: number) => request<CartResponse>(`/cart/${userId}`),
  addToCart: (payload: { user_id: number; product_id: number; quantity: number }) =>
    request('/cart/items', { method: 'POST', body: JSON.stringify(payload) }),
  createOrder: (user_id: number) => request('/orders', { method: 'POST', body: JSON.stringify({ user_id }) }),
  chat: (payload: { user_id: number; message: string }) =>
    request<ChatResponse>('/chat', { method: 'POST', body: JSON.stringify(payload) }),
}
