import { useEffect, useState } from 'react'
import { api } from '../shared/api/client'
import type { CartResponse } from '../shared/types/api'
import { useTelegramUserId } from '../hooks/useTelegramUser'

export function CartPage() {
  const userId = useTelegramUserId()
  const [cart, setCart] = useState<CartResponse | null>(null)

  async function load() {
    setCart(await api.getCart(userId))
  }

  async function checkout() {
    await api.createOrder(userId)
    await load()
    alert('Заказ создан')
  }

  useEffect(() => {
    void load()
  }, [])

  const total = cart?.items.reduce((sum, item) => sum + Number(item.product.price) * item.quantity, 0) ?? 0

  return (
    <section>
      <h2>Корзина</h2>
      {!cart?.items.length && <p>Корзина пуста</p>}
      <div className="stack">
        {cart?.items.map((item) => (
          <div key={item.id} className="card row between">
            <div>
              <div>{item.product.name}</div>
              <small>{item.quantity} x {item.product.price} {item.product.currency}</small>
            </div>
            <strong>{(Number(item.product.price) * item.quantity).toFixed(2)}</strong>
          </div>
        ))}
      </div>
      <div className="row between">
        <strong>Итого: {total.toFixed(2)} RUB</strong>
        <button disabled={!cart?.items.length} onClick={() => void checkout()}>Оформить</button>
      </div>
    </section>
  )
}
