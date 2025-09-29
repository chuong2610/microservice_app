from db.redis_client import redis_client
import json
import logging
from redis.exceptions import ConnectionError, TimeoutError

logger = logging.getLogger(__name__)

class TokenRepository:
    def save_refresh_token(self, user_info: dict, token: str, expire: int = 60*60*24*7):
        try:
            key = f"refresh:{user_info['id']}"
            value = json.dumps({
                "token": token,
                "role": user_info.get("role")
            })
            redis_client.setex(key, expire, value)
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"Redis connection error when saving refresh token: {e}")
            raise Exception("Unable to save refresh token - Redis connection failed")

    def get_refresh_token(self, user_id: str):
        try:
            data = redis_client.get(f"refresh:{user_id}")
            if data:
                return json.loads(data)
            return None
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"Redis connection error when getting refresh token: {e}")
            return None

    def revoke_refresh_token(self, user_id: str):
        try:
            redis_client.delete(f"refresh:{user_id}")
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"Redis connection error when revoking refresh token: {e}")
                    
