from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Order, OrderItem
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate
from app.services.user_service import UserService


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.cart_repo = CartRepository(db)
        self.order_repo = OrderRepository(db)
        self.user_service = UserService(db)

    def create_order(self, payload: OrderCreate) -> Order:
        user = self.user_service.ensure_by_telegram(payload.user_id)
        cart_items = self.cart_repo.list_by_user(user.id)
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        total = sum((Decimal(item.quantity) * item.product.price for item in cart_items), Decimal("0"))
        order = Order(user_id=user.id, status="created", total_amount=total)
        order_items = [
            OrderItem(product_id=item.product_id, quantity=item.quantity, unit_price=item.product.price, order_id=0)
            for item in cart_items
        ]
        created = self.order_repo.create_order(order, order_items)

        for item in cart_items:
            self.db.delete(item)
        self.db.commit()
        return created
