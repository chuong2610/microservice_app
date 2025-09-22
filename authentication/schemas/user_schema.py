from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class BaseResponse(BaseModel):
    status_code: int
    data: dict
    message: str

class TokenDecodeRequest(BaseModel):
    token: str

class TokenRefreshRequest(BaseModel):
    user_id: str
    refresh_token: str

