from db.database import create_redis_client
from repositories.user_repository import UserRepository
from services.user_service import UserService


class UserServiceFactory:
    @staticmethod
    def create():
        """Create and configure UserService with its dependencies"""
        user_repository = UserRepository()
        redis = create_redis_client()
        return UserService(user_repository, redis)

        