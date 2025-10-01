from pydantic import BaseModel
from typing import Any, Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
    role: Optional[str] = "user"

class LoginWithGoogleRequest(BaseModel):
    id_token: str    

class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any] = None

class TokenDecodeRequest(BaseModel):
    token: str

class TokenRefreshRequest(BaseModel):
    user_id: str
    refresh_token: str

