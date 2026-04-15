from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analytics_router, cart_router, chat_router, health_router, orders_router, products_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(health_router)
    app.include_router(products_router)
    app.include_router(cart_router)
    app.include_router(orders_router)
    app.include_router(chat_router)
    app.include_router(analytics_router)
    return app


app = create_app()
