from __future__ import annotations

import json
from typing import Any

import orjson
from redis import Redis

from app.config import settings


_redis_client: Redis | None = None


def get_redis_client() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis_client


def cache_set(key: str, value: Any, ttl_seconds: int = 60) -> None:
    data = orjson.dumps(value).decode()
    get_redis_client().setex(key, ttl_seconds, data)


def cache_get(key: str) -> Any | None:
    raw = get_redis_client().get(key)
    if raw is None:
        return None
    return json.loads(raw)


