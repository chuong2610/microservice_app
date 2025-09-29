from db.database import cart_container

class CartRepository:
    def create_cart(self, cart_data):
        cart_container.create_item(body=cart_data)

    def get_cart_by_id(self, cart_id):
        query = f"SELECT * FROM c WHERE c.id = '{cart_id}'"
        items = list(cart_container.query_items(query=query, enable_cross_partition_query=True))
        return items[0] if items else None

    def get_carts_by_user(self, user_id):
        query = f"SELECT * FROM c WHERE c.user_id = '{user_id}'"
        return list(cart_container.query_items(query=query, enable_cross_partition_query=True))

    def update_cart(self, cart_id, update_data):
        existing_cart = self.get_cart_by_id(cart_id)
        if not existing_cart:
            return None
        for key, value in update_data.items():
            existing_cart[key] = value
        cart_container.replace_item(item=existing_cart, body=existing_cart)
        return existing_cart
