from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.routers.users import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    buyer = db.query(models.User).filter(models.User.email == current_user).first()
    if buyer.role != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can make orders")

    product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.quantity < 1:
        raise HTTPException(status_code=400, detail="Product out of stock")

    seller = db.query(models.User).filter(models.User.id == product.owner_id).first()

    new_order = models.Order(
        product_id=product.id,
        buyer_id=buyer.id,
        seller_id=seller.id,
        status="completed"
    )

    product.quantity -= 1
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/", response_model=list[schemas.OrderOut])
def get_orders(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.email == current_user).first()
    if user.role == "buyer":
        return db.query(models.Order).filter(models.Order.buyer_id == user.id).all()
    elif user.role == "seller":
        return db.query(models.Order).filter(models.Order.seller_id == user.id).all()
    else:
        raise HTTPException(status_code=403, detail="Invalid role")
