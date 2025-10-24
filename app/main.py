from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, auth, products, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FoodService API")

@app.get("/")
def root():
    return {"message": "Welcome to FoodService!"}

# Подключаем роутеры
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
