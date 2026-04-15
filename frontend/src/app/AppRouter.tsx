import { Link, Navigate, Route, Routes } from 'react-router-dom'
import { CatalogPage } from '../pages/CatalogPage'
import { CartPage } from '../pages/CartPage'
import { ChatPage } from '../pages/ChatPage'
import { OrderSummaryPage } from '../pages/OrderSummaryPage'

export function AppRouter() {
  return (
    <main className="layout">
      <header>
        <h1>AI Store Mini App</h1>
        <nav className="row">
          <Link to="/catalog">Каталог</Link>
          <Link to="/cart">Корзина</Link>
          <Link to="/chat">AI-чат</Link>
          <Link to="/order-summary">Заказ</Link>
        </nav>
      </header>

      <Routes>
        <Route path="/catalog" element={<CatalogPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/order-summary" element={<OrderSummaryPage />} />
        <Route path="*" element={<Navigate to="/catalog" replace />} />
      </Routes>
    </main>
  )
}
