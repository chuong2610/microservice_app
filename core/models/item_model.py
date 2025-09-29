from datetime import date, datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel

class Item(BaseModel):
    id: str 
    title: str
    abstract: str
    content: str
    images: list[str] = []
    tags: list[str] = []
    category: str
    meta_field: dict
    createdAt: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    updatedAt: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    status: str = "draft"  
    author_id: str
