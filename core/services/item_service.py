from datetime import datetime
import json
import uuid
from zoneinfo import ZoneInfo

import redis
from repositories.item_repository import ItemRepository
from schemas.item_schema import ItemDTO, ItemDetailDTO

class ItemService:
    def __init__(self, item_repository: ItemRepository, redis: redis.Redis):
        self.item_repository = item_repository
        self.redis = redis

    def get_item_by_id(self, item_id):
        item = self.item_repository.get_item_by_id(item_id)
        if item:
            return self.map_item_to_detail_dto(item)
        return None

    def get_items(self, page_number=1, page_size=10):
        redis_key = f"items:page:{page_number}:size:{page_size}"
        cached_data = self.redis.get(redis_key)
        if cached_data:
            return json.loads(cached_data)

        data = self.item_repository.get_items(page_number, page_size)
        data['items'] = self.map_items_to_dto(data.get("items", []))
        
        # Convert Pydantic models to dictionaries for JSON serialization
        cache_data = data.copy()
        try:
            cache_data['items'] = [item.model_dump() for item in cache_data['items']]
        except AttributeError:
            # Fallback for older Pydantic versions
            cache_data['items'] = [item.dict() for item in cache_data['items']]
        
        redis_key = f"items:page:{page_number}:size:{page_size}"
        self.redis.set(redis_key, json.dumps(cache_data, default=str), ex=300)
        return data
    
    def get_items_by_author(self, author_id: str, page_number=1, page_size=10):
        redis_key = f"items:author:{author_id}:page:{page_number}:size:{page_size}"
        cached_data = self.redis.get(redis_key)
        if cached_data:
            return json.loads(cached_data)

        data = self.item_repository.get_items_by_author(author_id, page_number, page_size)
        data['items'] = self.map_items_to_dto(data.get("items", []))
        
        # Convert Pydantic models to dictionaries for JSON serialization
        cache_data = data.copy()
        try:
            cache_data['items'] = [item.model_dump() for item in cache_data['items']]
        except AttributeError:
            # Fallback for older Pydantic versions
            cache_data['items'] = [item.dict() for item in cache_data['items']]
        
        redis_key = f"items:author:{author_id}:page:{page_number}:size:{page_size}"
        self.redis.set(redis_key, json.dumps(cache_data, default=str), ex=300)
        return data
    
    def get_items_by_category(self, category: str, page_number=1, page_size=10):
        redis_key = f"items:category:{category}:page:{page_number}:size:{page_size}"
        cached_data = self.redis.get(redis_key)
        if cached_data:
            return json.loads(cached_data)

        data = self.item_repository.get_items_by_category(category, page_number, page_size)
        data['items'] = self.map_items_to_dto(data.get("items", []))
        
        # Convert Pydantic models to dictionaries for JSON serialization
        cache_data = data.copy()
        try:
            cache_data['items'] = [item.model_dump() for item in cache_data['items']]
        except AttributeError:
            # Fallback for older Pydantic versions
            cache_data['items'] = [item.dict() for item in cache_data['items']]
        
        redis_key = f"items:category:{category}:page:{page_number}:size:{page_size}"
        self.redis.set(redis_key, json.dumps(cache_data, default=str), ex=300)
        return data

    def create_item(self, item_data: dict):
        item_data['id'] = uuid.uuid4().hex
        item_data['status'] = 'published'
        item_data['createdAt'] = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
        item_data['updatedAt'] = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
        new_item = self.item_repository.create_item(item_data)
        self.redis.delete("items:page:*:size:*")
        self.redis.delete(f"items:author:{item_data['authorId']}:page:*:size:*")
        self.redis.delete(f"items:category:{item_data['category']}:page:*:size:*")

        return self.map_item_to_detail_dto(new_item)
    
    def update_item(self, item_id: str, update_data: dict):
        update_data['updatedAt'] = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
        updated_item = self.item_repository.update_item(item_id, update_data)
        if updated_item:
            self.redis.delete("items:page:*:size:*")
            self.redis.delete(f"items:author:{updated_item['authorId']}:page:*:size:*")
            self.redis.delete(f"items:category:{updated_item['category']}:page:*:size:*")
            return self.map_item_to_detail_dto(updated_item)
        return None
    
    def delete_item(self, item_id: str):
        item = self.item_repository.get_item_by_id(item_id)
        success = self.item_repository.delete_item(item_id)
        if success:
            self.redis.delete("items:page:*:size:*")
            self.redis.delete(f"items:author:{item['authorId']}:page:*:size:*")
            self.redis.delete(f"items:category:{item['category']}:page:*:size:*")
        return success

    def map_item_to_detail_dto(self, item: dict):
        return ItemDetailDTO(**item)    
    
    def map_items_to_dto(self, items: list[dict]):
        return [ItemDTO(**item) for item in items]