from pydantic import BaseModel
from typing import Any, Optional


class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any] = None
    