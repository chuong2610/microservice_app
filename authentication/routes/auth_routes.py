from math import log
from fastapi import APIRouter, Depends, Header
from schemas.user_schema import LoginRequest, BaseResponse, LoginWithGoogleRequest, TokenDecodeRequest, TokenRefreshRequest
from factories.auth_factory import get_auth_service


router = APIRouter()
service = get_auth_service()

@router.post("/login")
def login(user: LoginRequest, app_id: str =  Header(None)):
    try:
        tokens = service.login(user.email, user.password, app_id)
        return BaseResponse(status_code=200, data=tokens, message="Login successful")
    except Exception as e:
        return BaseResponse(status_code=401, message=str(e))

@router.post("/decode-token")
def decode_token(token_request: TokenDecodeRequest, app_id: str =  Header(None)):
    try:
        payload = service.decode_token(token_request.token, app_id)
        return BaseResponse(status_code=200, data=payload, message="Token decoded successfully")
    except Exception as e:
        return BaseResponse(status_code=400, message=str(e))

@router.post("/refresh")
def refresh_token(request: TokenRefreshRequest, app_id: str =  Header(None)):
    try:
        tokens = service.refresh(request.user_id, request.refresh_token, app_id)
        return BaseResponse(status_code=200, data=tokens, message="Token refreshed successfully")
    except Exception as e:
        return BaseResponse(status_code=401, message=str(e))

@router.post("/logout")
def logout(user_id: str):
    try:
        result = service.logout(user_id)
        return BaseResponse(status_code=200, data=result, message="Logout successful")
    except Exception as e:
        return BaseResponse(status_code=400, message=str(e))
    
@router.post("/register")
def register(user_data: dict, app_id: str = Header(None)):
    try:
        new_user = service.register(user_data, app_id)
        return BaseResponse(status_code=201, data=new_user, message="User registered successfully")
    except Exception as e:
        return BaseResponse(status_code=400, message=str(e))   
    
@router.post("/login/google")
async def login_with_google(login: LoginWithGoogleRequest, app_id: str = Header(None)):
    try:
        tokens = await service.login_with_google(login.id_token, app_id)
        return BaseResponse(status_code=200, data=tokens, message="Login with Google successful")
    except Exception as e:
        return BaseResponse(status_code=400, message=str(e))    

@router.get("/health")
def health_check():
    return BaseResponse(status_code=200, data={"status": "healthy"}, message="Service is healthy")

