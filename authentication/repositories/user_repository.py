from db.database import container
import uuid
from models.users_model import User

class UserRepository:
    def get_user_by_email(self, email: str):
        query = f"SELECT * FROM c WHERE c.email = '{email}'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return items[0] if items else None
    
    def get_user_by_id(self, user_id: str):
        query = f"SELECT * FROM c WHERE c.id = '{user_id}'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return items[0] if items else None
