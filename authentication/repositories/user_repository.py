from db.database import container
import uuid
from models.user_model import User
from typing import Optional

class UserRepository:
    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email address"""
        try:
            query = "SELECT * FROM c WHERE c.email = @email"
            parameters = [{"name": "@email", "value": email}]
            items = list(container.query_items(
                query=query, 
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            return items[0] if items else None
        except Exception:
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        try:
            query = "SELECT * FROM c WHERE c.id = @user_id"
            parameters = [{"name": "@user_id", "value": user_id}]
            items = list(container.query_items(
                query=query,
                parameters=parameters, 
                enable_cross_partition_query=True
            ))
            return items[0] if items else None
        except Exception:
            return None

    def create_user(self, user_data: dict) -> dict:
        """Create a new user"""
        try:
            user_data['id'] = uuid.uuid4().hex
            user_data['role'] = user_data.get('role', 'user')
            user_data['is_active'] = user_data.get('is_active', True)
            
            created_user = container.create_item(body=user_data)
            return created_user
        except Exception as e:
            raise Exception(f"Failed to create user: {str(e)}")

    def user_exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        return self.get_user_by_email(email) is not None
