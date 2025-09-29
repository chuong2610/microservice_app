from db.database import container


class ItemRepository:
    def get_item_by_id(self, item_id):
        try:
            item = container.read_item(item=item_id, partition_key=item_id)
            return item
        except Exception:
            return None
    
    def get_items(self, page_number=1, page_size=10, app_id: str = None):
        count_query = "SELECT VALUE COUNT(1) FROM c WHERE c.status != 'deleted' and c.app_id=@app_id" 
        total_items = list(container.query_items(
            query=count_query,
            parameters=[{"name": "@app_id", "value": app_id}],
            enable_cross_partition_query=True
        ))[0]

        total_pages = (total_items + page_size - 1) // page_size
        offset = (page_number - 1) * page_size

        query = f"SELECT * FROM c OFFSET {offset} LIMIT {page_size} WHERE c.status != 'deleted' and c.app_id=@app_id"
        items = list(container.query_items(
            query=query,
            parameters=[{"name": "@app_id", "value": app_id}],
            enable_cross_partition_query=True
        ))

        return {
            "items": items,
            "page_number": page_number,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }

    def get_items_by_author(self, author_id: str, page_number=1, page_size=10, app_id: str = None):
        count_query = "SELECT VALUE COUNT(1) FROM c WHERE c.author_id=@author_id and c.app_id=@app_id"
        total_items = list(container.query_items(
            query=count_query,
            parameters=[{"name": "@author_id", "value": author_id} ,{"name": "@app_id", "value": app_id}],
            enable_cross_partition_query=True
        ))[0]

        total_pages = (total_items + page_size - 1) // page_size
        offset = (page_number - 1) * page_size

        query = f"SELECT * FROM c WHERE c.author_id=@author_id OFFSET {offset} LIMIT {page_size} and c.app_id=@app_id"
        items = list(container.query_items(
            query=query,
            parameters=[{"name": "@author_id", "value": author_id}, {"name": "@app_id", "value": app_id}],
            enable_cross_partition_query=True
        ))

        return {
            "items": items,
            "page_number": page_number,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    
    def get_items_by_category(self, category: str, page_number=1, page_size=10 , app_id: str = None):
        count_query = "SELECT VALUE COUNT(1) FROM c WHERE c.category = @cat and c.app_id=@app_id"
        total_items = list(container.query_items(
            query=count_query,
            parameters=[{"name": "@cat", "value": category}, {"name": "@app_id", "value": app_id}],
            enable_cross_partition_query=True
        ))[0]

        total_pages = (total_items + page_size - 1) // page_size
        offset = (page_number - 1) * page_size

        query = f"SELECT * FROM c WHERE c.category = @cat OFFSET {offset} LIMIT {page_size} and c.app_id=@app_id"
        items = list(container.query_items(
            query=query,
            parameters=[{"name": "@cat", "value": category}, {"name": "@app_id", "value": app_id}],
            enable_cross_partition_query=True
        ))

        return {
            "items": items,
            "page_number": page_number,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }

    def create_item(self, user_data: dict):
        create_item = container.create_item(body=user_data)
        return create_item
    
    def update_item(self, item_id: str, update_data: dict):
        existing_item = self.get_item_by_id(item_id)
        if not existing_item:
            return None
        for key, value in update_data.items():
            existing_item[key] = value
        updated_item = container.replace_item(item=existing_item['id'], body=existing_item)
        return updated_item
    
    def delete_item(self, item_id: str):
        try:  
            item = self.get_item_by_id(item_id)
            if not item:
                return False
            item['status'] = 'deleted'
            container.replace_item(item=item['id'], body=item)
            return True
        except Exception:
            return False