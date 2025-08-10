from __future__ import annotations

from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.repositories import record_repository
from app.services.cache import cache_set, cache_get


def compute_achievement_rate(session: Session, user_id: int, window_days: int = 30) -> float:
    end = date.today()
    start = end - timedelta(days=window_days - 1)
    days_with_records = record_repository.count_record_days_in_range(session, user_id, start, end)
    rate = round(min(100.0, max(0.0, (days_with_records / float(window_days)) * 100.0)), 2)

    cache_set(_cache_key(user_id), {"value": rate, "window_days": window_days}, ttl_seconds=3600)
    return rate


def get_cached_achievement_rate(user_id: int) -> dict | None:
    return cache_get(_cache_key(user_id))


def _cache_key(user_id: int) -> str:
    return f"user:{user_id}:achievement_rate"


