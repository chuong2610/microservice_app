import uuid
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
from settings import settings
import utils as auth_utils
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def login(self, email: str, password: str, app_id: str = None):
        user = self.user_repo.get_user_by_email(email, app_id)
        if not user or not auth_utils.verify_password(password, user["password"]):
            raise Exception("Invalid credentials")
        user_payload = {"id": user["id"], "role": user.get("role")}
        payload = {"sub": user_payload, "app_id": app_id}
        access_token = auth_utils.create_access_token(payload)
        refresh_token = auth_utils.create_refresh_token(payload)
        self.token_repo.save_refresh_token(user, refresh_token)
        
        # Return user data along with tokens for frontend display
        user_data = {
            "id": user["id"],
            "email": user["email"],
            "full_name": user.get("full_name"),
            "role": user.get("role", "user"),
            "avatar_url": user.get("avatar_url"),
            "is_active": user.get("is_active", True),
            "created_at": user.get("created_at")
        }
        
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "user": user_data
        }
    
    def decode_token(self, token: str, app_id: str = None):
        payload = auth_utils.decode_token(token)
        if payload.get("app_id") != app_id:
            raise Exception("Token app_id mismatch")
        return payload

    def refresh(self, user_id: str, refresh_token: str, app_id: str = None):
        user = self.user_repo.get_user_by_id(user_id, app_id)
        if not user:
            raise Exception("User not found")
        stored = self.token_repo.get_refresh_token(user_id)
        if not stored or stored["token"] != refresh_token:
            raise Exception("Invalid refresh token")
        payload = auth_utils.decode_token(refresh_token)
        if payload.get("app_id") != app_id:
            raise Exception("Token app_id mismatch")
        new_access_token = auth_utils.create_access_token(payload)
        new_refresh_token = auth_utils.create_refresh_token(payload)
        self.token_repo.save_refresh_token(user, new_refresh_token)
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}

    def logout(self, user_id: str):
        self.token_repo.revoke_refresh_token(user_id)
        return {"message": "Logged out successfully"}
    
    def register(self, user_data: dict, app_id: str = None):
        existing_user = self.user_repo.get_user_by_email(user_data["email"], app_id)
        if existing_user and existing_user.get("password") != None:
            raise Exception("User already exists")
        hashed_password = auth_utils.hash_password(user_data["password"])
        user_data["password"] = hashed_password
        user_data["role"] = user_data.get("role", "user")
        user_data["id"] = str(uuid.uuid4())  
        user_data["app_id"] = app_id
        new_user = self.user_repo.create_user(user_data)
        return {"id": new_user["id"], "email": new_user["email"], "role": new_user["role"]}
    

    async def login_with_google(self, id_token_str: str, app_id: str = None):
        try:
            CLIENT_ID = settings.GOOGLE_CLIENT_ID  
            idinfo = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), CLIENT_ID)

            email = idinfo.get("email")
            if not email:
                raise ValueError("Token không chứa email hợp lệ")

            user = self.user_repo.get_user_by_email(email, app_id)
            if not user:
                user_data = {
                    "id": str(uuid.uuid4()),
                    "full_name": idinfo.get("name", ""),
                    "email": email,
                    "avatar_url": idinfo.get("picture"),
                    "role": "user",
                    "app_id": app_id
                }
                user = self.user_repo.create_user(user_data)

            user_id = user.get("user_id") or user.get("id")
            token = auth_utils.create_access_token({"sub": {"id": user_id, "role": user.get("role")}, "app_id": app_id})

            return {
                "access_token": token, 
                "user_id": user_id, 
                "role": user.get("role", "user")
            }

        except ValueError as e:
            raise ValueError(f"Token không hợp lệ: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Lỗi lấy Google user info: {str(e)}") from e