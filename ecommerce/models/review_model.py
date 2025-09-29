from pydantic import BaseModel


class Review(BaseModel):
    id: int
    item_id: int
    user_id: int
    rating: int
    comment: str