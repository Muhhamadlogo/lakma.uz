import { useState } from 'react'
import { api } from '../shared/api/client'
import type { ChatResponse } from '../shared/types/api'
import { useTelegramUserId } from '../hooks/useTelegramUser'

export function ChatPage() {
  const userId = useTelegramUserId()
  const [message, setMessage] = useState('Подбери мне аксессуары из кожи до 5000 рублей')
  const [response, setResponse] = useState<ChatResponse | null>(null)

  async function send() {
    const data = await api.chat({ user_id: userId, message })
    setResponse(data)
  }

  return (
    <section>
      <h2>AI-чат стилиста</h2>
      <textarea value={message} onChange={(e) => setMessage(e.target.value)} rows={4} />
      <button onClick={() => void send()}>Отправить</button>

      {response && (
        <div className="card">
          <p><strong>Intent:</strong> {response.intent}</p>
          <p><strong>Agent:</strong> {response.agent}</p>
          <p>{response.reply}</p>
          <ul>
            {response.products.map((p) => (
              <li key={p.id}>{p.name} — {p.price} {p.currency}</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  )
}
