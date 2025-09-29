import uuid
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
import utils as auth_utils

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
        return {"access_token": access_token, "refresh_token": refresh_token}
    
    def decode_token(self, token: str, app_id: str = None):
        payload = auth_utils.decode_token(token)
        if payload.get("app_id") != app_id:
            raise Exception("Token app_id mismatch")
        return payload

    def refresh(self, user_id: str, refresh_token: str, app_id: str = None):
        user = self.user_repo.get_user_by_id(user_id, app_id)
        stored = self.token_repo.get_refresh_token(user_id)
        if not stored or stored["token"] != refresh_token:
            raise Exception("Invalid refresh token")
        payload = auth_utils.decode_token(refresh_token)
        new_access_token = auth_utils.create_access_token(payload)
        refresh_token = auth_utils.create_refresh_token(payload)
        self.token_repo.save_refresh_token(user, refresh_token)
        return {"access_token": new_access_token, "refresh_token": refresh_token}

    def logout(self, user_id: str):
        self.token_repo.revoke_refresh_token(user_id)
        return {"message": "Logged out successfully"}
    
    def register(self, user_data: dict, app_id: str = None):
        existing_user = self.user_repo.get_user_by_email(user_data["email"], app_id)
        if existing_user:
            raise Exception("User already exists")
        hashed_password = auth_utils.hash_password(user_data["password"])
        user_data["password"] = hashed_password
        user_data["role"] = "user"  # Default role
        user_data["id"] = str(uuid.uuid4())  
        user_data["app_id"] = app_id
        new_user = self.user_repo.create_user(user_data)
        return {"id": new_user["id"], "email": new_user["email"], "role": new_user["role"]}
    