from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from pydantic import BaseModel


class ItemDTO(BaseModel):
    id: str
    title: str
    abstract: str
    images: list[str] = []
    meta_field: Optional[dict] = None
    createdAt: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    updatedAt: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    author_id: str


class ItemDetailDTO(ItemDTO):
    content: str
    category: list[str] = []


class ItemCreateRequest(BaseModel):
    title: str
    abstract: str
    content: str
    images: list[str] = []
    tags: list[str] = []
    category: list[str] = []
    meta_field: Optional[dict] = None
    author_id: str