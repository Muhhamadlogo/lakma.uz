from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel
from app.schemas.product import ProductRead


class CartItemCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemRead(ORMModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    created_at: datetime
    product: ProductRead


class CartRead(BaseModel):
    user_id: int
    items: list[CartItemRead]
