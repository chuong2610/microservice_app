from db.database import container
import uuid
from models.user_model import User

class UserRepository:
    def get_user_by_email(self, email: str, app_id: str = None):
        query = f"SELECT * FROM c WHERE c.email = '{email}' and c.app_id = '{app_id}'" 
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return items[0] if items else None
    
    def get_user_by_id(self, user_id: str, app_id: str = None):
        query = f"SELECT * FROM c WHERE c.id = '{user_id}' and c.app_id = '{app_id}'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return items[0] if items else None  
    
    def create_user(self, user: dict):
        container.create_item(body=user)
        return user.dict()
