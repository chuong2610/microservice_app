from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
import utils as auth_utils

class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def login(self, email: str, password: str):
        user = self.user_repo.get_user_by_email(email)
        if not user or not auth_utils.verify_password(password, user["hashed_password"]):
            raise Exception("Invalid credentials")
        access_token = auth_utils.create_access_token({"sub": user["id"]})
        refresh_token = auth_utils.create_refresh_token({"sub": user["id"]})
        return {"access_token": access_token, "refresh_token": refresh_token}
    
    def decode_token(self, token: str):
        return auth_utils.decode_token(token)

    def refresh(self, user_id: str, refresh_token: str):
        stored = self.token_repo.get_refresh_token(user_id)
        if not stored or stored["token"] != refresh_token:
            raise Exception("Invalid refresh token")
        payload = auth_utils.decode_token(refresh_token)
        new_access_token = auth_utils.create_access_token({"sub": payload["sub"]})
        return {"access_token": new_access_token, "refresh_token": refresh_token}

    def logout(self, user_id: str):
        self.token_repo.revoke_refresh_token(user_id)
        return {"message": "Logged out successfully"}