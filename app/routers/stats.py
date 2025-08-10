from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.stats_service import get_cached_achievement_rate, compute_achievement_rate
from app.tasks.stats_tasks import compute_achievement_rate_task, compute_achievement_rate_all_users

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/achievement-rate")
def get_achievement_rate(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Get cached achievement rate for current user"""
    cached = get_cached_achievement_rate(current_user.id)
    if cached:
        return cached
    
    # If not cached, calculate fresh value
    rate = compute_achievement_rate(db, current_user.id)
    return {"value": rate, "window_days": 30}


@router.get("/achievement-rate/user/{user_id}")
def get_user_achievement_rate(
    user_id: int,
    window_days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Get achievement rate for specific user (admin only)"""
    # TODO: Add admin role check if needed
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")
    
    cached = get_cached_achievement_rate(user_id)
    if cached and cached.get("window_days") == window_days:
        return cached
    
    # Calculate fresh value
    rate = compute_achievement_rate(db, user_id, window_days)
    return {"value": rate, "window_days": window_days}


@router.post("/achievement-rate/trigger")
def trigger_achievement_rate_calculation(
    user_id: int | None = None,
    window_days: int = 30,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Manually trigger achievement rate calculation"""
    if user_id:
        # Calculate for specific user
        task = compute_achievement_rate_task.delay(user_id, window_days)
        return {"message": f"Calculation triggered for user {user_id}", "task_id": task.id}
    else:
        # Calculate for all users
        task = compute_achievement_rate_all_users.delay(window_days)
        return {"message": "Calculation triggered for all users", "task_id": task.id}


