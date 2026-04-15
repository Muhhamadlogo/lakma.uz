from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductRead
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(query: str | None = None, category_id: int | None = None, db: Session = Depends(get_db)) -> list[ProductRead]:
    service = ProductService(db)
    return service.list_products(query=query, category_id=category_id)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductRead:
    service = ProductService(db)
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductRead)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> ProductRead:
    return ProductService(db).create_product(payload)
