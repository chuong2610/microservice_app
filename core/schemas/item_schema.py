from datetime import datetime
from typing import Optional, Any
from zoneinfo import ZoneInfo
from pydantic import BaseModel, model_validator


class ItemDTO(BaseModel):
    id: str
    title: str
    abstract: str
    images: list[str] = []
    meta_field: Optional[dict] = None
    createdAt: Optional[datetime] = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    updatedAt: Optional[datetime] = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    author_id: Optional[str] = None


class ItemDetailDTO(ItemDTO):
    content: Optional[str] = ""
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