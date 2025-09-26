from redis import Redis
from settings import settings


def create_redis_client():
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD or None,
        ssl=settings.REDIS_SSL,
        ssl_cert_reqs=None if settings.REDIS_SSL else None,
        db=0,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
        health_check_interval=30
    )
