from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int


class Cart(BaseModel):
    id: str
    user_id: str
    items: List[CartItem] = []
    total_price: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None