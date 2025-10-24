from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/admin", tags=["Admin"])

# Главная панель
@router.get("/", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    products = db.query(models.Product).all()
    orders = db.query(models.Order).all()

    html = """
    <html>
    <head>
        <title>FoodService Admin Panel</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #fafafa; }}
            h1 {{ color: #333; }}
            h2 {{ color: #555; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 40px; background: white; box-shadow: 0 0 6px rgba(0,0,0,0.1); }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #f4f4f4; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .section {{ margin-bottom: 50px; }}
            .container {{ max-width: 1000px; margin: auto; }}
            form {{ display:inline; }}
            button {{ background:#007bff; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer; }}
            button.delete {{ background:#dc3545; }}
            button:hover {{ opacity:0.9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FoodService Admin Panel</h1>

            <div class="section">
                <h2>Users</h2>
                <table>
                    <tr><th>ID</th><th>Email</th><th>Role</th><th>Actions</th></tr>
                    {}
                </table>
                <form method="post" action="/admin/create_user">
                    <input name="email" placeholder="email" required>
                    <input name="password" placeholder="password" required>
                    <select name="role">
                        <option value="buyer">buyer</option>
                        <option value="seller">seller</option>
                    </select>
                    <button type="submit">Add User</button>
                </form>
            </div>

            <div class="section">
                <h2>Products</h2>
                <table>
                    <tr><th>ID</th><th>Title</th><th>Price</th><th>Quantity</th><th>Owner ID</th><th>Actions</th></tr>
                    {}
                </table>
                <form method="post" action="/admin/create_product">
                    <input name="title" placeholder="title" required>
                    <input name="price" type="number" step="0.01" placeholder="price" required>
                    <input name="quantity" type="number" placeholder="quantity" value="1">
                    <input name="owner_id" type="number" placeholder="owner_id" required>
                    <button type="submit">Add Product</button>
                </form>
            </div>

            <div class="section">
                <h2>Orders</h2>
                <table>
                    <tr><th>ID</th><th>Buyer ID</th><th>Product ID</th><th>Created At</th></tr>
                    {}
                </table>
            </div>
        </div>
    </body>
    </html>
    """.format(
        "\n".join(
            f"<tr><td>{u.id}</td><td>{u.email}</td><td>{u.role}</td>"
            f"<td><form method='post' action='/admin/delete_user'><input type='hidden' name='user_id' value='{u.id}'><button class='delete'>Delete</button></form></td></tr>"
            for u in users
        ),
        "\n".join(
            f"<tr><td>{p.id}</td><td>{p.title}</td><td>{p.price}</td><td>{p.quantity}</td><td>{p.owner_id}</td>"
            f"<td><form method='post' action='/admin/delete_product'><input type='hidden' name='product_id' value='{p.id}'><button class='delete'>Delete</button></form></td></tr>"
            for p in products
        ),
        "\n".join(
            f"<tr><td>{o.id}</td><td>{o.buyer_id}</td><td>{o.product_id}</td><td>{o.created_at}</td></tr>"
            for o in orders
        ),
    )
    return HTMLResponse(content=html)


# ——— CRUD-действия ———

@router.post("/create_user")
def create_user(email: str = Form(...), password: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    new_user = models.User(email=email, hashed_password=password, role=role)
    db.add(new_user)
    db.commit()
    return RedirectResponse("/admin", status_code=303)


@router.post("/delete_user")
def delete_user(user_id: int = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return RedirectResponse("/admin", status_code=303)


@router.post("/create_product")
def create_product(title: str = Form(...), price: float = Form(...), quantity: int = Form(...), owner_id: int = Form(...), db: Session = Depends(get_db)):
    new_product = models.Product(title=title, price=price, quantity=quantity, owner_id=owner_id)
    db.add(new_product)
    db.commit()
    return RedirectResponse("/admin", status_code=303)


@router.post("/delete_product")
def delete_product(product_id: int = Form(...), db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return RedirectResponse("/admin", status_code=303)
