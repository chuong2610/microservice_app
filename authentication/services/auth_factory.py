import token
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService

def get_auth_service():
    user_repo = UserRepository()
    token_repo = TokenRepository()
    return AuthService(user_repo, token_repo)
