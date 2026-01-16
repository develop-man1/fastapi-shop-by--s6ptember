from .products import router as product_router
from .categories import router as categories_router
from .cart import router as cart_router

__all__ = ["product_router", "categories_router", "cart_router"]