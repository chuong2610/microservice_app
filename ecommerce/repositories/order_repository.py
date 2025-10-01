from db.database import order_container

class OrderRepository:
    def create_order(self, order_data):
        return order_container.create_item(body=order_data)
    
    def get_order_by_id(self, order_id):
        try:
            order = order_container.read_item(item=order_id, partition_key=order_id)
            return order
        except Exception as e:
            print(f"Error retrieving order: {e}")
            return None

    def get_orders_by_user(self, user_id):
        query = f"SELECT * FROM o WHERE o.user_id = '{user_id}'"
        return list(order_container.query_items(query=query, enable_cross_partition_query=True))

        

