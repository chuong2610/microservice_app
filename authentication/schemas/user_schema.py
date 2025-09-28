from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    full_name: str = Field(..., max_length=100, min_length=1)
    email: EmailStr
    password: str = Field(...)
    avatar_url: Optional[str] = None

class BaseResponse(BaseModel):
    status_code: int
    data: dict | None = None
    message: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenDecodeRequest(BaseModel):
    token: str

class TokenRefreshRequest(BaseModel):
    user_id: str
    refresh_token: str

class LogoutRequest(BaseModel):
    user_id: str

