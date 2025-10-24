from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.routers.users import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()
    new_product = models.Product(**product.model_dump(), owner_id=user.id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/", response_model=List[schemas.ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products
