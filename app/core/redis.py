import redis.asyncio as redis
import json
from app.core.config import settings as settings


redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_cache(key: str):
    value = await redis_client.get(key)
    if value is not None:
        return json.loads(value)
    return None


async def set_cache(key: str, value, ttl: int = 3600):
    await redis_client.set(key, json.dumps(value), ex=ttl)


async def delete_cache(key: str):
    await redis_client.delete(key)

