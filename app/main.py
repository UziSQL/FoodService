from fastapi import FastAPI

app = FastAPI(title="FoodService API")

@app.get("/")
def root():
    return {"message": "Welcome to FoodService!"}

from app.routers import users
app.include_router(users.router)

from app.routers import auth
app.include_router(auth.router)
