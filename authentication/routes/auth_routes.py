from fastapi import APIRouter, HTTPException
from schemas.user_schema import (
    LoginRequest, 
    RegisterRequest,
    BaseResponse, 
    TokenDecodeRequest, 
    TokenRefreshRequest,
    LogoutRequest
)
from factories.auth_factory import get_auth_service

router = APIRouter()
service = get_auth_service()

@router.post("/register")
def register(register_request: RegisterRequest):
    """Register a new user"""
    try:
        tokens = service.register(register_request)
        return BaseResponse(
            status_code=201, 
            data=tokens.model_dump(), 
            message="Registration successful"
        )
    except Exception as e:
        return BaseResponse(
            status_code=400, 
            data=None, 
            message=str(e)
        )

@router.post("/login")
def login(login_request: LoginRequest):
    """Authenticate user and return tokens"""
    try:
        tokens = service.login(login_request.email, login_request.password)
        return BaseResponse(
            status_code=200, 
            data=tokens.model_dump(), 
            message="Login successful"
        )
    except Exception as e:
        return BaseResponse(
            status_code=401, 
            data=None, 
            message=str(e)
        )

@router.post("/decode-token")
def decode_token(token_request: TokenDecodeRequest):
    """Decode and validate JWT token"""
    try:
        payload = service.decode_token(token_request.token) 
        return BaseResponse(
            status_code=200, 
            data=payload, 
            message="Token decoded successfully"
        )
    except Exception as e:
        return BaseResponse(
            status_code=401, 
            data=None, 
            message=str(e)
        )

@router.post("/refresh")
def refresh_token(request: TokenRefreshRequest):
    """Refresh access token using refresh token"""
    try:
        tokens = service.refresh(request.user_id, request.refresh_token)
        return BaseResponse(
            status_code=200, 
            data=tokens.model_dump(), 
            message="Token refreshed successfully"
        )
    except Exception as e:
        return BaseResponse(
            status_code=401, 
            data=None, 
            message=str(e)
        )

@router.post("/logout")
def logout(logout_request: LogoutRequest):
    """Logout user by revoking refresh token"""
    try:
        result = service.logout(logout_request.user_id)
        return BaseResponse(
            status_code=200, 
            data=result, 
            message="Logout successful"
        )
    except Exception as e:
        return BaseResponse(
            status_code=400, 
            data=None, 
            message=str(e)
        )

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "authentication-service"}
