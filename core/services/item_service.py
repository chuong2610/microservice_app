from datetime import datetime
import json
import uuid
from zoneinfo import ZoneInfo

from repositories.item_repository import ItemRepository
from schemas.item_schema import ItemDTO, ItemDetailDTO

class ItemService:
    def __init__(self, item_repository: ItemRepository, redis_client=None):
        self.item_repository = item_repository
        self.redis = redis_client
    
    def _cache_get(self, key):
        try:
            return self.redis.get(key) if self.redis else None
        except:
            return None
    
    def _cache_set(self, key, value, ttl=300):
        try:
            if self.redis:
                self.redis.set(key, json.dumps(value, default=str), ex=ttl)
        except:
            pass
    
    def _cache_delete(self, pattern):
        try:
            if self.redis:
                keys = self.redis.keys(pattern)
                if keys:
                    self.redis.delete(*keys)
        except:
            pass

    def get_item_by_id(self, item_id):
        item = self.item_repository.get_item_by_id(item_id)
        if item:
            return self.map_item_to_detail_dto(item)
        return None

    def get_items(self, page_number=1, page_size=10, app_id: str = None):
        cache_key = f"items:page:{page_number}:size:{page_size}:app_id:{app_id}"
        cached = self._cache_get(cache_key)
        if cached:
            return json.loads(cached)

        data = self.item_repository.get_items(page_number, page_size, app_id=app_id)
        data['items'] = self.map_items_to_dto(data.get("items", []))
        
        # Cache serializable version
        cache_data = data.copy()
        cache_data['items'] = [item.model_dump() for item in cache_data['items']]
        self._cache_set(cache_key, cache_data)
        
        return data

    def get_items_by_author(self, author_id: str, page_number=1, page_size=10, app_id: str = None):
        cache_key = f"items:author:{author_id}:page:{page_number}:size:{page_size}"
        cached = self._cache_get(cache_key)
        if cached:
            return json.loads(cached)
        
        data = self.item_repository.get_items_by_author(author_id, page_number, page_size , app_id=app_id)
        data['items'] = self.map_items_to_dto(data.get("items", []))
        
        # Cache serializable version
        cache_data = data.copy()
        cache_data['items'] = [item.model_dump() for item in cache_data['items']]
        self._cache_set(cache_key, cache_data)
        
        return data
    
    def get_items_by_category(self, category: str, page_number=1, page_size=10 , app_id: str = None):
        cache_key = f"items:category:{category}:page:{page_number}:size:{page_size}:app_id:{app_id}"
        cached = self._cache_get(cache_key)
        if cached:
            return json.loads(cached)

        data = self.item_repository.get_items_by_category(category, page_number, page_size, app_id=app_id)
        data['items'] = self.map_items_to_dto(data.get("items", []))
        
        # Cache serializable version
        cache_data = data.copy()
        cache_data['items'] = [item.model_dump() for item in cache_data['items']]
        self._cache_set(cache_key, cache_data)
        
        return data

    def create_item(self, item_data: dict):
        item_data['id'] = uuid.uuid4().hex
        item_data['status'] = 'published'
        item_data['createdAt'] = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
        item_data['updatedAt'] = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
        new_item = self.item_repository.create_item(item_data)
        
        # Smart cache invalidation
        self._cache_delete("items:page:*")
        if 'author_id' in item_data:
            self._cache_delete(f"items:author:{item_data['author_id']}:*")
        if 'category' in item_data:
            self._cache_delete(f"items:category:{item_data['category']}:*")
        
        return self.map_item_to_detail_dto(new_item)
    
    def update_item(self, item_id: str, update_data: dict):
        update_data['updatedAt'] = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
        updated_item = self.item_repository.update_item(item_id, update_data)
        if updated_item:
            # Smart cache invalidation
            self._cache_delete("items:page:*")
            author_id = updated_item.get('author_id') or updated_item.get('authorId')
            if author_id:
                self._cache_delete(f"items:author:{author_id}:*")
            if 'category' in updated_item:
                self._cache_delete(f"items:category:{updated_item['category']}:*")
            
            return self.map_item_to_detail_dto(updated_item)
        return None
    
    def delete_item(self, item_id: str):
        item = self.item_repository.get_item_by_id(item_id)
        success = self.item_repository.delete_item(item_id)
        if success:
            # Smart cache invalidation
            self._cache_delete("items:page:*")
            author_id = item.get('author_id') or item.get('authorId')
            if author_id:
                self._cache_delete(f"items:author:{author_id}:*")
            if 'category' in item:
                self._cache_delete(f"items:category:{item['category']}:*")
        return success

    def map_item_to_detail_dto(self, item: dict):
        return ItemDetailDTO(**item)    
    
    def map_items_to_dto(self, items: list[dict]):
        return [ItemDTO(**item) for item in items]