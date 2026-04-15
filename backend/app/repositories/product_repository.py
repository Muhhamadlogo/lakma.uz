from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_products(self, *, query: str | None = None, category_id: int | None = None) -> list[Product]:
        stmt: Select[tuple[Product]] = select(Product).where(Product.is_active.is_(True))
        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)
        if query:
            like_query = f"%{query.lower()}%"
            stmt = stmt.where(Product.name.ilike(like_query))
        return list(self.db.scalars(stmt.order_by(Product.created_at.desc())).all())

    def get(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
