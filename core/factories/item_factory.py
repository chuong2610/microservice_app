import re
from db import redis_client
from repositories.item_repository import ItemRepository
from services.item_service import ItemService


class ItemServiceFactory:
    @staticmethod
    def create():
        item_repository = ItemRepository()
        redis = redis_client.create_redis_client()
        return ItemService(item_repository, redis)