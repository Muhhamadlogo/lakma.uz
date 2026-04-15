from sqlalchemy.orm import Session

from app.models import Order, OrderItem


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order, items: list[OrderItem]) -> Order:
        self.db.add(order)
        self.db.flush()
        for item in items:
            item.order_id = order.id
            self.db.add(item)
        self.db.commit()
        self.db.refresh(order)
        return order
