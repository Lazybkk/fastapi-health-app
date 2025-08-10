from __future__ import annotations

from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.repositories import record_repository
from app.services.cache import cache_set, cache_get


def compute_achievement_rate(session: Session, user_id: int, window_days: int = 30) -> float:
    """
    Calculate achievement rate based on goals completed vs goals set.
    Formula: (Total Goals Completed / Total Goals Set) × 100%
    """
    end = date.today()
    start = end - timedelta(days=window_days - 1)
    
    # Count completed goals within the window
    completed_goals = record_repository.count_completed_goals_by_user(
        session, user_id, date_from=start, date_to=end
    )
    
    # Count total active goals
    total_goals = record_repository.count_total_goals_by_user(session, user_id)
    
    # Calculate rate
    if total_goals == 0:
        rate = 0.0
    else:
        rate = round(min(100.0, max(0.0, (completed_goals / float(total_goals)) * 100.0)), 2)

    cache_set(_cache_key(user_id), {
        "value": rate, 
        "window_days": window_days,
        "completed_goals": completed_goals,
        "total_goals": total_goals
    }, ttl_seconds=3600)
    return rate


def get_cached_achievement_rate(user_id: int) -> dict | None:
    return cache_get(_cache_key(user_id))


def _cache_key(user_id: int) -> str:
    return f"user:{user_id}:achievement_rate"


