from typing import Optional
from db.database import container


class UserRepository:
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get a user by ID"""
        try:
            user = container.read_item(item=user_id, partition_key=user_id)
            return user
        except Exception:
            return None

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get a user by email address"""
        try:
            query = "SELECT * FROM c WHERE c.email = @email"
            parameters = [{"name": "@email", "value": email}]
            
            users = list(container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            return users[0] if users else None
        except Exception:
            return None

    def get_users(self, page_number: int = 1, page_size: int = 10) -> dict:
        """Get paginated list of users"""
        # Count total users
        count_query = "SELECT VALUE COUNT(1) FROM c WHERE c.is_active = true"
        total_users = list(container.query_items(
            query=count_query,
            enable_cross_partition_query=True
        ))[0]

        total_pages = (total_users + page_size - 1) // page_size
        offset = (page_number - 1) * page_size

        # Get users with pagination, only active users
        query = f"SELECT * FROM c WHERE c.is_active = true OFFSET {offset} LIMIT {page_size}"
        users = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        return {
            "users": users,
            "page_number": page_number,
            "page_size": page_size,
            "total_users": total_users,
            "total_pages": total_pages
        }

    def create_user(self, user_data: dict) -> dict:
        """Create a new user"""
        try:
            created_user = container.create_item(body=user_data) 
            return created_user
        except Exception as e:
            raise Exception(f"Failed to create user: {str(e)}")
    
    def update_user(self, user_id: str, update_data: dict) -> Optional[dict]:
        """Update user information"""
        try:
            existing_user = self.get_user_by_id(user_id)
            if not existing_user:
                return None
            
            # Update fields
            for key, value in update_data.items():
                existing_user[key] = value
            
            updated_user = container.replace_item(
                item=existing_user['id'], 
                body=existing_user
            )
            return updated_user
        except Exception:
            return None

    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user (soft delete)"""
        try:
            existing_user = self.get_user_by_id(user_id)
            if not existing_user:
                return False
            
            existing_user['is_active'] = False
            container.replace_item(item=existing_user['id'], body=existing_user)
            return True
        except Exception:
            return False

    def activate_user(self, user_id: str) -> bool:
        """Activate a user"""
        try:
            existing_user = self.get_user_by_id(user_id)
            if not existing_user:
                return False
            
            existing_user['is_active'] = True
            container.replace_item(item=existing_user['id'], body=existing_user)
            return True
        except Exception:
            return False
    
    def delete_user(self, user_id: str) -> bool:
        """Hard delete a user"""
        try:  
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            container.delete_item(item=user_id, partition_key=user_id)
            return True
        except Exception:
            return False

            