from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, auth, products, orders
from app.routers import admin


Base.metadata.create_all(bind=engine)

app = FastAPI(title="FoodService API")

@app.get("/")
def root():
    return {"message": "Welcome to FoodService!"}

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(admin.router)

