import pickle
from typing import Any

import redis  # type: ignore


def get_redis_client():
    return redis.Redis(host='redis', port=6379, db=0)


class RedisCache:
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis_client = redis_client
        self.ttl = 600

    def get(self, key: str) -> Any:
        data = self.redis_client.get(key)
        if data is not None:
            if data == b'changed':
                return None
            return pickle.loads(data)
        return None

    def set(self, key: str, value: Any) -> bool:
        if type(value) is str:
            return self.redis_client.setex(key, self.ttl, value)
        return self.redis_client.setex(key, self.ttl, pickle.dumps(value))

    def delete(self, key: str) -> int:
        return self.redis_client.delete(key)
