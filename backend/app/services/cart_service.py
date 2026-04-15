from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import CartItem
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.services.user_service import UserService


class CartService:
    def __init__(self, db: Session):
        self.repo = CartRepository(db)
        self.product_repo = ProductRepository(db)
        self.user_service = UserService(db)

    def get_cart(self, user_id: int) -> list[CartItem]:
        user = self.user_service.ensure_by_telegram(user_id)
        return self.repo.list_by_user(user.id)

    def add_item(self, payload: CartItemCreate) -> CartItem:
        user = self.user_service.ensure_by_telegram(payload.user_id)
        product = self.product_repo.get(payload.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        existing = self.repo.find_user_product(user.id, payload.product_id)
        if existing:
            existing.quantity += payload.quantity
            return self.repo.save(existing)

        item = CartItem(user_id=user.id, product_id=payload.product_id, quantity=payload.quantity)
        return self.repo.save(item)

    def update_item(self, item_id: int, payload: CartItemUpdate) -> CartItem:
        item = self.repo.get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        item.quantity = payload.quantity
        return self.repo.save(item)

    def remove_item(self, item_id: int) -> None:
        item = self.repo.get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        self.repo.delete(item)
