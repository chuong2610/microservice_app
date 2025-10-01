import json
import uuid
from datetime import timedelta
from typing import Optional

import redis
from repositories.user_repository import UserRepository
from schemas.user_schema import (
    UserDTO, UserDetailDTO, UserCreateRequest
)
from settings import settings
from utils import hash_password


class UserService:
    def __init__(self, user_repository: UserRepository, redis: redis.Redis):
        self.user_repository = user_repository
        self.redis = redis

    def get_user_by_id(self, user_id: str, app_id: str = None) -> Optional[UserDetailDTO]:
        """Get a user by ID"""
        user = self.user_repository.get_user_by_id(user_id, app_id=app_id)
        if user:
            return self.map_user_to_detail_dto(user)
        return None

    def get_users(self, page_number: int = 1, page_size: int = 10, app_id: str = None) -> dict:
        """Get paginated list of users"""
        redis_key = f"users:page:{page_number}:size:{page_size}:app:{app_id}"
        
        # Try to get from cache, but continue if Redis is down
        try:
            cached_data = self.redis.get(redis_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis error (continuing without cache): {e}")
            # Continue without caching

        data = self.user_repository.get_users(page_number, page_size, app_id=app_id)
        data['users'] = self.map_users_to_dto(data.get("users", []))
        
        # Convert Pydantic models to dictionaries for JSON serialization
        cache_data = data.copy()
        try:
            cache_data['users'] = [user.model_dump() for user in cache_data['users']]
        except AttributeError:
            # Fallback for older Pydantic versions
            cache_data['users'] = [user.dict() for user in cache_data['users']]
        
        # Try to cache the result, but continue if Redis is down
        try:
            self.redis.set(redis_key, json.dumps(cache_data, default=str), ex=settings.USER_CACHE_TTL)
        except Exception as e:
            print(f"Redis caching error (continuing anyway): {e}")
        
        return data
    
    def create_user(self, user_request: UserCreateRequest) -> UserDetailDTO:
        """Create a new user"""
        user_data = user_request.model_dump()
        user_data['id'] = uuid.uuid4().hex
        
        # Check if user with this email already exists
        existing_user = self.user_repository.get_user_by_email(user_data['email'])
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash password before storing
        user_data['password'] = hash_password(user_data['password'])
        
        new_user = self.user_repository.create_user(user_data)
        
        # Clear cache
        self._clear_users_cache()
        
        return self.map_user_to_detail_dto(new_user)
    
    def update_user(self, user_id: str, update_data: dict) -> Optional[UserDetailDTO]:
        """Update a user"""
        # Remove fields that shouldn't be updated directly
        restricted_fields = ['id', 'password']  
        for field in restricted_fields:
            update_data.pop(field, None)
        
        updated_user = self.user_repository.update_user(user_id, update_data)
        if updated_user:
            self._clear_users_cache()
            return self.map_user_to_detail_dto(updated_user)
        return None
    
    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user (soft delete)"""
        success = self.user_repository.deactivate_user(user_id)
        if success:
            self._clear_users_cache()
        return success

    def activate_user(self, user_id: str) -> bool:
        """Activate a user"""
        success = self.user_repository.activate_user(user_id)
        if success:
            self._clear_users_cache()
        return success

    def delete_user(self, user_id: str) -> bool:
        """Hard delete a user"""
        success = self.user_repository.delete_user(user_id)
        if success:
            self._clear_users_cache()
        return success

    def _clear_users_cache(self):
        """Clear all users cache"""
        # Try to clear cache, but continue if Redis is down
        try:
            keys = self.redis.keys("users:page:*")
            if keys:
                self.redis.delete(*keys)
        except Exception as e:
            print(f"Redis cache clear error (continuing anyway): {e}")

    def map_user_to_detail_dto(self, user: dict) -> UserDetailDTO:
        """Map user dict to UserDetailDTO"""
        return UserDetailDTO(**user)    
    
    def map_users_to_dto(self, users: list[dict]) -> list[UserDTO]:
        """Map list of user dicts to UserDTO list"""
        return [UserDTO(**user) for user in users]

    def get_user_by_email(self, email: str) -> Optional[UserDetailDTO]:
        """Get a user by email"""
        user = self.user_repository.get_user_by_email(email)
        if user:
            return self.map_user_to_detail_dto(user)
        return None

