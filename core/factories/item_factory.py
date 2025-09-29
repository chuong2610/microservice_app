from repositories.item_repository import ItemRepository
from services.item_service import ItemService
from db.redis_client import create_redis_client


class ItemServiceFactory:
    @staticmethod
    def create():
        item_repository = ItemRepository()
        
        # Try to create Redis client, but don't fail if it's unavailable
        redis_client = None
        try:
            redis_client = create_redis_client()
            redis_client.ping()  # Test connection
        except:
            pass  # Redis unavailable, continue without caching
        
        return ItemService(item_repository, redis_client)

        