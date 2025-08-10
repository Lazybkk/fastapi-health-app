from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_current_user
from app.models.user import User
from app.services.stats_service import get_cached_achievement_rate
from app.tasks.stats_tasks import compute_achievement_rate_task


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/stats/achievement-rate/enqueue")
def enqueue_achievement_rate(current_user: User = Depends(get_current_user), window_days: int = Query(30, ge=1, le=365)):
    task = compute_achievement_rate_task.delay(current_user.id, window_days)
    return {"task_id": task.id}


@router.get("/stats/achievement-rate")
def get_achievement_rate(current_user: User = Depends(get_current_user)):
    cached = get_cached_achievement_rate(current_user.id)
    return cached or {"value": None}


