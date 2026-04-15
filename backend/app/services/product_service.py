from sqlalchemy.orm import Session

from app.models import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def list_products(self, query: str | None = None, category_id: int | None = None) -> list[Product]:
        return self.repo.list_products(query=query, category_id=category_id)

    def get_product(self, product_id: int) -> Product | None:
        return self.repo.get(product_id)

    def create_product(self, payload: ProductCreate) -> Product:
        product = Product(**payload.model_dump())
        return self.repo.create(product)
