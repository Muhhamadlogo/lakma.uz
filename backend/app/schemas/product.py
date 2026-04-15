from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.common import ORMModel


class ProductBase(BaseModel):
    name: str
    description: str = ""
    category_id: int | None = None
    price: Decimal
    currency: str = "RUB"
    color: str | None = None
    size: str | None = None
    material: str | None = None
    stock: int = 0
    gender: str | None = None
    season: str | None = None
    image_url: str | None = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductRead(ORMModel, ProductBase):
    id: int
    created_at: datetime
