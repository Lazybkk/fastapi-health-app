from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.records import (
    BodyRecordCreate, BodyRecordRead, BodyRecordUpdate,
    MealCreate, MealRead, MealUpdate,
    ExerciseCreate, ExerciseRead, ExerciseUpdate,
    DiaryCreate, DiaryRead, DiaryUpdate,
    GoalCreate, GoalRead, GoalUpdate,
    GoalProgressCreate, GoalProgressRead, GoalProgressUpdate,
)
from app.schemas.common import Pagination
from app.services.record_service import (
    body_record_service, meal_service, exercise_service, diary_service,
    goal_service, goal_progress_service
)

router = APIRouter(prefix="/records", tags=["records"])


# Body Records
@router.get("/body-records", response_model=Pagination[BodyRecordRead])
def list_body_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    date_from: str | None = Query(None, description="YYYY-MM-DD"),
    date_to: str | None = Query(None, description="YYYY-MM-DD"),
):
    """List body records for current user with pagination and date filters"""
    from datetime import datetime
    date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date() if date_from else None
    date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date() if date_to else None
    
    return body_record_service.list_records(
        db, current_user.id, limit=limit, offset=offset,
        date_from=date_from_obj, date_to=date_to_obj
    )


@router.post("/body-records", response_model=BodyRecordRead, status_code=201)
def create_body_record(
    record: BodyRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new body record"""
    return body_record_service.create_record(db, current_user.id, record.model_dump())


@router.get("/body-records/{record_id}", response_model=BodyRecordRead)
def get_body_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific body record"""
    record = body_record_service.get_record(db, current_user.id, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Body record not found")
    return record


@router.patch("/body-records/{record_id}", response_model=BodyRecordRead)
def update_body_record(
    record_id: int,
    record_update: BodyRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a body record"""
    record = body_record_service.update_record(
        db, current_user.id, record_id, record_update.model_dump(exclude_unset=True)
    )
    if not record:
        raise HTTPException(status_code=404, detail="Body record not found")
    return record


@router.delete("/body-records/{record_id}", status_code=204)
def delete_body_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a body record"""
    success = body_record_service.delete_record(db, current_user.id, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Body record not found")


# Goals
@router.get("/goals", response_model=Pagination[GoalRead])
def list_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    is_active: bool | None = Query(None),
):
    """List goals for current user with pagination and active filter"""
    return goal_service.list_records(
        db, current_user.id, limit=limit, offset=offset, is_active=is_active
    )


@router.post("/goals", response_model=GoalRead, status_code=201)
def create_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new goal"""
    return goal_service.create_record(db, current_user.id, goal.model_dump())


@router.get("/goals/{goal_id}", response_model=GoalRead)
def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific goal"""
    goal = goal_service.get_record(db, current_user.id, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.patch("/goals/{goal_id}", response_model=GoalRead)
def update_goal(
    goal_id: int,
    goal_update: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a goal"""
    goal = goal_service.update_record(
        db, current_user.id, goal_id, goal_update.model_dump(exclude_unset=True)
    )
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.delete("/goals/{goal_id}", status_code=204)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a goal"""
    success = goal_service.delete_record(db, current_user.id, goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")


# Goal Progress
@router.get("/goals/{goal_id}/progress", response_model=Pagination[GoalProgressRead])
def list_goal_progress(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    date_from: str | None = Query(None, description="YYYY-MM-DD"),
    date_to: str | None = Query(None, description="YYYY-MM-DD"),
):
    """List progress for a specific goal"""
    # Verify goal belongs to user
    goal = goal_service.get_record(db, current_user.id, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    from datetime import datetime
    date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date() if date_from else None
    date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date() if date_to else None
    
    return goal_progress_service.list_records(
        db, goal_id, limit=limit, offset=offset,
        date_from=date_from_obj, date_to=date_to_obj
    )


@router.post("/goals/{goal_id}/progress", response_model=GoalProgressRead, status_code=201)
def create_goal_progress(
    goal_id: int,
    progress: GoalProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create progress for a specific goal"""
    # Verify goal belongs to user
    goal = goal_service.get_record(db, current_user.id, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    result = goal_progress_service.create_record(db, goal_id, progress.model_dump())
    
    # Trigger achievement rate calculation when goal progress is created
    from app.tasks.stats_tasks import compute_achievement_rate_task
    compute_achievement_rate_task.delay(current_user.id)
    
    return result


@router.get("/goals/{goal_id}/progress/{progress_id}", response_model=GoalProgressRead)
def get_goal_progress(
    goal_id: int,
    progress_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific goal progress"""
    # Verify goal belongs to user
    goal = goal_service.get_record(db, current_user.id, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    progress = goal_progress_service.get_record(db, goal_id, progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Goal progress not found")
    return progress


@router.patch("/goals/{goal_id}/progress/{progress_id}", response_model=GoalProgressRead)
def update_goal_progress(
    goal_id: int,
    progress_id: int,
    progress_update: GoalProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a goal progress"""
    # Verify goal belongs to user
    goal = goal_service.get_record(db, current_user.id, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    progress = goal_progress_service.update_record(
        db, goal_id, progress_id, progress_update.model_dump(exclude_unset=True)
    )
    if not progress:
        raise HTTPException(status_code=404, detail="Goal progress not found")
    return progress


@router.delete("/goals/{goal_id}/progress/{progress_id}", status_code=204)
def delete_goal_progress(
    goal_id: int,
    progress_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a goal progress"""
    # Verify goal belongs to user
    goal = goal_service.get_record(db, current_user.id, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    success = goal_progress_service.delete_record(db, goal_id, progress_id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal progress not found")


# Meals
@router.get("/meals", response_model=Pagination[MealRead])
def list_meals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    date_from: str | None = Query(None, description="YYYY-MM-DD"),
    date_to: str | None = Query(None, description="YYYY-MM-DD"),
    meal_type: str | None = Query(None),
):
    """List meals for current user with pagination and filters"""
    from datetime import datetime
    date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date() if date_from else None
    date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date() if date_to else None
    
    return meal_service.list_records(
        db, current_user.id, limit=limit, offset=offset,
        date_from=date_from_obj, date_to=date_to_obj, meal_type=meal_type
    )


@router.post("/meals", response_model=MealRead, status_code=201)
def create_meal(
    meal: MealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new meal"""
    return meal_service.create_record(db, current_user.id, meal.model_dump())


@router.get("/meals/{meal_id}", response_model=MealRead)
def get_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific meal"""
    meal = meal_service.get_record(db, current_user.id, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


@router.patch("/meals/{meal_id}", response_model=MealRead)
def update_meal(
    meal_id: int,
    meal_update: MealUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a meal"""
    meal = meal_service.update_record(
        db, current_user.id, meal_id, meal_update.model_dump(exclude_unset=True)
    )
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


@router.delete("/meals/{meal_id}", status_code=204)
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a meal"""
    success = meal_service.delete_record(db, current_user.id, meal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meal not found")


# Exercises
@router.get("/exercises", response_model=Pagination[ExerciseRead])
def list_exercises(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    date_from: str | None = Query(None, description="YYYY-MM-DD"),
    date_to: str | None = Query(None, description="YYYY-MM-DD"),
):
    """List exercises for current user with pagination and date filters"""
    from datetime import datetime
    date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date() if date_from else None
    date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date() if date_to else None
    
    return exercise_service.list_records(
        db, current_user.id, limit=limit, offset=offset,
        date_from=date_from_obj, date_to=date_to_obj
    )


@router.post("/exercises", response_model=ExerciseRead, status_code=201)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new exercise"""
    return exercise_service.create_record(db, current_user.id, exercise.model_dump())


@router.get("/exercises/{exercise_id}", response_model=ExerciseRead)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific exercise"""
    exercise = exercise_service.get_record(db, current_user.id, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.patch("/exercises/{exercise_id}", response_model=ExerciseRead)
def update_exercise(
    exercise_id: int,
    exercise_update: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an exercise"""
    exercise = exercise_service.update_record(
        db, current_user.id, exercise_id, exercise_update.model_dump(exclude_unset=True)
    )
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.delete("/exercises/{exercise_id}", status_code=204)
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an exercise"""
    success = exercise_service.delete_record(db, current_user.id, exercise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exercise not found")


# Diaries
@router.get("/diaries", response_model=Pagination[DiaryRead])
def list_diaries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    date_from: str | None = Query(None, description="YYYY-MM-DD"),
    date_to: str | None = Query(None, description="YYYY-MM-DD"),
):
    """List diaries for current user with pagination and date filters"""
    from datetime import datetime
    date_from_obj = datetime.strptime(date_from, "%Y-%m-%d").date() if date_from else None
    date_to_obj = datetime.strptime(date_to, "%Y-%m-%d").date() if date_to else None
    
    return diary_service.list_records(
        db, current_user.id, limit=limit, offset=offset,
        date_from=date_from_obj, date_to=date_to_obj
    )


@router.post("/diaries", response_model=DiaryRead, status_code=201)
def create_diary(
    diary: DiaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new diary entry"""
    return diary_service.create_record(db, current_user.id, diary.model_dump())


@router.get("/diaries/{diary_id}", response_model=DiaryRead)
def get_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific diary entry"""
    diary = diary_service.get_record(db, current_user.id, diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary


@router.patch("/diaries/{diary_id}", response_model=DiaryRead)
def update_diary(
    diary_id: int,
    diary_update: DiaryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a diary entry"""
    diary = diary_service.update_record(
        db, current_user.id, diary_id, diary_update.model_dump(exclude_unset=True)
    )
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary


@router.delete("/diaries/{diary_id}", status_code=204)
def delete_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a diary entry"""
    success = diary_service.delete_record(db, current_user.id, diary_id)
    if not success:
        raise HTTPException(status_code=404, detail="Diary not found")


