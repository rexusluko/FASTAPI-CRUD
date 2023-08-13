import pickle
from typing import Any

import redis.asyncio as redis  # type: ignore
from fastapi import Depends


def get_async_redis_pool():
    return redis.Redis(host='redis', port=6379, db=0)


async def get_async_redis_client(redis_pool: redis.Redis = Depends(get_async_redis_pool)):
    return redis_pool


class AsyncRedisCache:
    def __init__(self, redis_pool: redis.Redis = Depends(get_async_redis_pool)) -> None:
        self.redis_pool = redis_pool
        self.ttl = 1800

    async def get(self, key: str) -> Any:
        data = await self.redis_pool.get(key)
        if data and data != b'changed':
            return pickle.loads(data)
        return None

    async def set(self, key: str, value: Any) -> bool:
        if type(value) is str:
            return await self.redis_pool.setex(key, self.ttl, value)
        return await self.redis_pool.setex(key, self.ttl, pickle.dumps(value))

    async def delete(self, key: str) -> int:
        return await self.redis_pool.delete(key)
