from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/checkout", tags=["Checkout"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/success", response_class=HTMLResponse)
def payment_success(request: Request):

    return templates.TemplateResponse("payment_success.html", {"request": request})

@router.get("/{product_id}", response_class=HTMLResponse)
def checkout_page(request: Request, product_id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return templates.TemplateResponse("checkout.html", {
        "request": request,
        "product": product
    })

@router.post("/pay")
def simulate_payment(
    product_id: int = Form(...),
    buyer_id: int = Form(...),
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    buyer = db.query(models.User).filter(models.User.id == buyer_id).first()

    if not product or not buyer:
        raise HTTPException(status_code=400, detail="Invalid buyer or product")

    new_order = models.Order(
        product_id=product_id,
        buyer_id=buyer_id,
        seller_id=product.owner_id,
        status="completed"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return RedirectResponse(url="/checkout/success", status_code=303)
