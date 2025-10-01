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
    created_at: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    updated_at: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    status: str = "draft"  
    author_id: str
