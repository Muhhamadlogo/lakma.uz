from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.common import ORMModel


class OrderCreate(BaseModel):
    user_id: int


class OrderRead(ORMModel):
    id: int
    user_id: int
    status: str
    total_amount: Decimal
    created_at: datetime
