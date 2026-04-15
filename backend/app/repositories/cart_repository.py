from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import CartItem


class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_user(self, user_id: int) -> list[CartItem]:
        stmt = select(CartItem).options(joinedload(CartItem.product)).where(CartItem.user_id == user_id)
        return list(self.db.scalars(stmt).unique().all())

    def get(self, item_id: int) -> CartItem | None:
        return self.db.get(CartItem, item_id)

    def find_user_product(self, user_id: int, product_id: int) -> CartItem | None:
        stmt = select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
        return self.db.scalars(stmt).first()

    def save(self, item: CartItem) -> CartItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: CartItem) -> None:
        self.db.delete(item)
        self.db.commit()
