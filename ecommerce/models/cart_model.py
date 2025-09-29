from pydantic import BaseModel 


class Cart(BaseModel):
    id: int
    user_id: int
    items: list[dict]
    total_price: float