from pydantic import BaseModel


class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: dict | list | None = None 