from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "buyer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    title: str
    description: str | None = None
    price: float
    quantity: int = 1


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
