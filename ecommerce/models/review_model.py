from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Review(BaseModel):
    id: str
    product_id: str
    user_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: str
    user_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None