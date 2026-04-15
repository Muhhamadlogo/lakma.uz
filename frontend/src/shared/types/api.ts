export type Product = {
  id: number
  name: string
  description: string
  category_id: number | null
  price: string
  currency: string
  color: string | null
  size: string | null
  material: string | null
  stock: number
  gender: string | null
  season: string | null
  image_url: string | null
  is_active: boolean
  created_at: string
}

export type CartItem = {
  id: number
  user_id: number
  product_id: number
  quantity: number
  created_at: string
  product: Product
}

export type CartResponse = {
  user_id: number
  items: CartItem[]
}

export type ChatResponse = {
  intent: string
  agent: string
  reply: string
  products: Product[]
  artifacts: { artifact_type: string; content_json: Record<string, unknown> }[]
  run_id: number
}
