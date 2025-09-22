import redis
from settings import Settings


redis_client = redis.Redis(
    host=Settings.REDIS_HOST,
    port=Settings.REDIS_PORT,
    db=0,
    decode_responses=True
)
