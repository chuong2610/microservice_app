from fastapi import APIRouter, Depends
from schemas.user_schema import LoginRequest, BaseResponse, TokenDecodeRequest, TokenRefreshRequest
from services.auth_factory import get_auth_service


router = APIRouter()
service = get_auth_service()

@router.post("/login")
def login(user: LoginRequest):
    tokens = service.login(user.email, user.password)
    return BaseResponse(status_code=200, data=tokens, message="Login successful")

@router.post("/decode-token")
def decode_token(token_request: TokenDecodeRequest):
    payload = service.decode_token(token_request.token) 
    return BaseResponse(status_code=200, data=payload, message="Token decoded successfully")

@router.post("/refresh")
def refresh_token(request: TokenRefreshRequest):
    return service.refresh(request.user_id, request.refresh_token)

@router.get("/health")
def health_check():
    return {"status": "healthy"}
