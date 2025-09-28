import redis
from azure.cosmos import CosmosClient
from settings import settings

# Cosmos DB setup
client = CosmosClient(settings.COSMOS_ENDPOINT, settings.COSMOS_KEY)
database = client.create_database_if_not_exists(id=settings.COSMOS_DB_NAME)
container = database.create_container_if_not_exists(
    id=settings.COSMOS_CONTAINER_USERS,
    partition_key="/id",
    offer_throughput=400
)

# Redis client factory
def create_redis_client():
    """Create and return a Redis client instance"""
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        ssl=settings.REDIS_SSL,
        decode_responses=True
    )
