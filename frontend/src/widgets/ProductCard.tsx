import type { Product } from '../shared/types/api'

type Props = {
  product: Product
  onAdd: (productId: number) => void
}

export function ProductCard({ product, onAdd }: Props) {
  return (
    <article className="card">
      <img src={product.image_url || 'https://placehold.co/320x240'} alt={product.name} className="card-image" />
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <div className="meta">{product.material || 'Материал не указан'} · {product.color || 'Без цвета'}</div>
      <div className="row between">
        <strong>{product.price} {product.currency}</strong>
        <button onClick={() => onAdd(product.id)}>В корзину</button>
      </div>
    </article>
  )
}
