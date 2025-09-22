from db.redis import redis_client
import json

class TokenRepository:
    def save_refresh_token(self, user_info: dict, token: str, expire: int = 60*60*24*7):
        key = f"refresh:{user_info['id']}"
        value = json.dumps({
            "token": token,
            "username": user_info.get("username"),
            "role": user_info.get("role")
        })
        redis_client.setex(key, expire, value)

    def get_refresh_token(self, user_id: str):
        data = redis_client.get(f"refresh:{user_id}")
        if data:
            return json.loads(data)
        return None

    def revoke_refresh_token(self, user_id: str):
        redis_client.delete(f"refresh:{user_id}")
