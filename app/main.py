from fastapi import FastAPI

app = FastAPI(title="FoodService API")

@app.get("/")
def root():
    return {"message": "Welcome to FoodService!"}
