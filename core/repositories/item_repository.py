from httpx import delete
from db.database import container


class ItemRepository:
    def get_item_by_id(self, item_id):
        try:
            item = container.read_item(item=item_id, partition_key=item_id)
            return item
        except Exception:
            return None
    
    def get_items(self, page_number=1, page_size=10):
        count_query = "SELECT VALUE COUNT(1) FROM c"
        total_items = list(container.query_items(
            query=count_query,
            enable_cross_partition_query=True
        ))[0]

        total_pages = (total_items + page_size - 1) // page_size
        offset = (page_number - 1) * page_size

        query = f"SELECT * FROM c OFFSET {offset} LIMIT {page_size}"
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        return {
            "items": items,
            "page_number": page_number,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }

    def get_items_by_author(self, author_id: str, page_number=1, page_size=10):
        count_query = "SELECT VALUE COUNT(1) FROM c WHERE c.authorId=@authId"
        total_items = list(container.query_items(
            query=count_query,
            parameters=[{"name": "@authId", "value": author_id}],
            enable_cross_partition_query=True
        ))[0]

        total_pages = (total_items + page_size - 1) // page_size
        offset = (page_number - 1) * page_size

        query = f"SELECT * FROM c WHERE c.authorId=@authId OFFSET {offset} LIMIT {page_size}"
        items = list(container.query_items(
            query=query,
            parameters=[{"name": "@authId", "value": author_id}],
            enable_cross_partition_query=True
        ))

        return {
            "items": items,
            "page_number": page_number,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    
    def get_items_by_category(self, category: str, page_number=1, page_size=10):
        count_query = "SELECT VALUE COUNT(1) FROM c WHERE ARRAY_CONTAINS(c.category, @cat)"
        total_items = list(container.query_items(
            query=count_query,
            parameters=[{"name": "@cat", "value": category}],
            enable_cross_partition_query=True
        ))[0]

        total_pages = (total_items + page_size - 1) // page_size
        offset = (page_number - 1) * page_size

        query = f"SELECT * FROM c WHERE ARRAY_CONTAINS(c.category, @cat) OFFSET {offset} LIMIT {page_size}"
        items = list(container.query_items(
            query=query,
            parameters=[{"name": "@cat", "value": category}],
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