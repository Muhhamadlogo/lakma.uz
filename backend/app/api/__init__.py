from app.api.analytics import router as analytics_router
from app.api.cart import router as cart_router
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.orders import router as orders_router
from app.api.products import router as products_router

__all__ = [
    "health_router",
    "products_router",
    "cart_router",
    "orders_router",
    "chat_router",
    "analytics_router",
]
