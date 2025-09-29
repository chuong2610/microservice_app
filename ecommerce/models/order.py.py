from pydantic import BaseModel


class Order(BaseModel):
    id: int
    items: list[dict]
    total_price: float
    status: str