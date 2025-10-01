from db.database import cart_container
from datetime import datetime
import uuid


class CartRepository:
    async def get_cart(self, user_id: str):
        """Get cart by user_id, create if not exists"""
        try:
            query = f"SELECT * FROM c WHERE c.user_id = '{user_id}'"
            carts = list(cart_container.query_items(query=query, enable_cross_partition_query=True))
            
            if carts:
                return carts[0]
            
            # Create new cart if not exists
            cart_id = str(uuid.uuid4())
            cart_data = {
                "id": cart_id,
                "user_id": user_id,
                "items": [],
                "total_price": 0.0,
            }
            return cart_container.create_item(body=cart_data)
        except Exception as e:
            print(f"Error in get_cart: {e}")
            return None

    async def update_cart(self, user_id: str, cart_data: dict):
        """Update cart data"""
        try:
            cart_data["updated_at"] = datetime.utcnow().isoformat()
            cart_container.replace_item(item=cart_data["id"], body=cart_data)
            return cart_data
        except Exception as e:
            print(f"Error updating cart: {e}")
            return None

    def get_cart_by_id(self, cart_id):
        try:
            cart = cart_container.read_item(item=cart_id, partition_key=cart_id)
            return cart
        except Exception as e:
            print(f"Error retrieving cart: {e}")
            return None

    def create_cart(self, cart_data):
        return cart_container.create_item(body=cart_data)


