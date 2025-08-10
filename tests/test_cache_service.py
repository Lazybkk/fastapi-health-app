from __future__ import annotations

from app.services.cache import cache_set, cache_get


def test_cache_set_get_roundtrip():
    key = "test:key"
    payload = {"a": 1}
    cache_set(key, payload, ttl_seconds=10)
    val = cache_get(key)
    assert val == payload


