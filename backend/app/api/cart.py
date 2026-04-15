from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.cart import CartItemCreate, CartItemRead, CartItemUpdate, CartRead
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/{user_id}", response_model=CartRead)
def get_cart(user_id: int, db: Session = Depends(get_db)) -> CartRead:
    items = CartService(db).get_cart(user_id)
    return CartRead(user_id=user_id, items=items)


@router.post("/items", response_model=CartItemRead)
def add_cart_item(payload: CartItemCreate, db: Session = Depends(get_db)) -> CartItemRead:
    return CartService(db).add_item(payload)


@router.patch("/items/{item_id}", response_model=CartItemRead)
def update_cart_item(item_id: int, payload: CartItemUpdate, db: Session = Depends(get_db)) -> CartItemRead:
    return CartService(db).update_item(item_id, payload)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(item_id: int, db: Session = Depends(get_db)) -> Response:
    CartService(db).remove_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
