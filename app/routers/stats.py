from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.stats_service import compute_achievement_rate, get_cached_achievement_rate
from app.tasks.stats_tasks import compute_achievement_rate_task

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/achievement-rate")
def get_achievement_rate(
    window_days: int = Query(30, ge=1, le=365, description="Number of days to calculate achievement rate for"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get current user's achievement rate.
    
    Formula: (Total Goals Completed / Total Goals Set) × 100%
    
    The achievement rate shows how well the user is progressing toward their health goals.
    """
    # Try to get from cache first
    cached = get_cached_achievement_rate(current_user.id)
    if cached and cached.get("window_days") == window_days:
        return {
            "achievement_rate": cached["value"],
            "window_days": window_days,
            "completed_goals": cached.get("completed_goals", 0),
            "total_goals": cached.get("total_goals", 0),
            "cached": True
        }
    
    # Calculate fresh
    rate = compute_achievement_rate(db, current_user.id, window_days)
    
    # Get the cached data that was just set
    cached = get_cached_achievement_rate(current_user.id)
    
    return {
        "achievement_rate": rate,
        "window_days": window_days,
        "completed_goals": cached.get("completed_goals", 0) if cached else 0,
        "total_goals": cached.get("total_goals", 0) if cached else 0,
        "cached": False
    }


@router.get("/achievement-rate/user/{user_id}")
def get_achievement_rate_for_user(
    user_id: int,
    window_days: int = Query(30, ge=1, le=365, description="Number of days to calculate achievement rate for"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get achievement rate for a specific user (admin-like access).
    
    Formula: (Total Goals Completed / Total Goals Set) × 100%
    """
    # For now, allow any authenticated user to view others' stats
    # In production, you might want to add role-based access control
    
    # Try to get from cache first
    cached = get_cached_achievement_rate(user_id)
    if cached and cached.get("window_days") == window_days:
        return {
            "user_id": user_id,
            "achievement_rate": cached["value"],
            "window_days": window_days,
            "completed_goals": cached.get("completed_goals", 0),
            "total_goals": cached.get("total_goals", 0),
            "cached": True
        }
    
    # Calculate fresh
    rate = compute_achievement_rate(db, user_id, window_days)
    
    # Get the cached data that was just set
    cached = get_cached_achievement_rate(user_id)
    
    return {
        "user_id": user_id,
        "achievement_rate": rate,
        "window_days": window_days,
        "completed_goals": cached.get("completed_goals", 0) if cached else 0,
        "total_goals": cached.get("total_goals", 0) if cached else 0,
        "cached": False
    }


@router.post("/achievement-rate/trigger")
def trigger_achievement_rate_calculation(
    user_id: int | None = Query(None, description="Specific user ID, or None for all users"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Manually trigger achievement rate calculation.
    
    - If user_id is provided: calculate for that specific user
    - If user_id is None: calculate for all users (admin function)
    """
    if user_id is not None:
        # Calculate for specific user
        compute_achievement_rate_task.delay(user_id)
        return {"message": f"Achievement rate calculation triggered for user {user_id}"}
    else:
        # Calculate for all users
        from app.tasks.stats_tasks import compute_achievement_rate_all_users
        compute_achievement_rate_all_users.delay()
        return {"message": "Achievement rate calculation triggered for all users"}


