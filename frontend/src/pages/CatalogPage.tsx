import { useEffect, useState } from 'react'
import { ProductCard } from '../widgets/ProductCard'
import { api } from '../shared/api/client'
import type { Product } from '../shared/types/api'
import { useTelegramUserId } from '../hooks/useTelegramUser'

export function CatalogPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const userId = useTelegramUserId()

  async function load() {
    setLoading(true)
    setError('')
    try {
      setProducts(await api.listProducts(query))
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void load()
  }, [])

  async function add(productId: number) {
    await api.addToCart({ user_id: userId, product_id: productId, quantity: 1 })
    alert('Добавлено в корзину')
  }

  return (
    <section>
      <h2>Каталог</h2>
      <div className="row">
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Поиск по товарам" />
        <button onClick={() => void load()}>Найти</button>
      </div>
      {loading && <p>Загрузка...</p>}
      {error && <p className="error">{error}</p>}
      {!loading && !products.length && <p>Товары не найдены</p>}
      <div className="grid">
        {products.map((p) => (
          <ProductCard key={p.id} product={p} onAdd={add} />
        ))}
      </div>
    </section>
  )
}
