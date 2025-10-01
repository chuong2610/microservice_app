from email.mime import image
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CartItemSchema(BaseModel):
    product_id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    image: str = Field( description="Product image URL")
    price: float = Field(..., gt=0, description="Product price")
    quantity: int = Field(..., gt=0, description="Item quantity")


class AddToCartRequest(BaseModel):
    product_id: str = Field(..., description="Product ID to add")
    name: str = Field(..., description="Product name")
    image: str = Field( description="Product image URL")
    price: float = Field(..., gt=0, description="Product price")
    quantity: int = Field(1, gt=0, description="Quantity to add")


class UpdateQuantityRequest(BaseModel):
    product_id: str = Field(..., description="Product ID to update")
    quantity: int = Field(..., ge=0, description="New quantity (0 to remove)")


class RemoveFromCartRequest(BaseModel):
    product_id: str = Field(..., description="Product ID to remove")


class CartResponse(BaseModel):
    id: str
    user_id: str
    items: List[CartItemSchema] = []
    total_price: float = 0.0



class CartSummaryResponse(BaseModel):
    items_count: int
    total_price: float
    items: List[CartItemSchema] = []