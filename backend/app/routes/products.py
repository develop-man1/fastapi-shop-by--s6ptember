from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.product_services import ProductService
from ..schemas.product import ProductListResponse, ProductResponse


router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

@router.get("", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_all_products()