from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.records import (
    BodyRecordCreate,
    BodyRecordRead,
    BodyRecordUpdate,
    MealCreate,
    MealRead,
    MealUpdate,
    ExerciseCreate,
    ExerciseRead,
    ExerciseUpdate,
    DiaryCreate,
    DiaryRead,
    DiaryUpdate,
)
from app.schemas.common import Pagination
from app.services import record_service
from app.tasks.stats_tasks import compute_achievement_rate_task


router = APIRouter(dependencies=[Depends(get_current_user)])


# Body Records
@router.get("/body-records", response_model=Pagination[BodyRecordRead])
def list_body_records(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int | None = Query(None, ge=1, le=100),
    offset: int = Query(0, ge=0),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
):
    return record_service.list_body_records(
        session,
        current_user.id,
        limit=limit,
        offset=offset,
        date_from=date_from,
        date_to=date_to,
    )


@router.post("/body-records", response_model=BodyRecordRead, status_code=201)
def create_body_record(
    payload: BodyRecordCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = record_service.create_body_record(session, current_user.id, payload)
    # Trigger achievement rate calculation
    compute_achievement_rate_task.delay(current_user.id)
    return result


@router.patch("/body-records/{record_id}", response_model=BodyRecordRead)
def update_body_record(
    record_id: int,
    payload: BodyRecordUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    try:
        return record_service.update_body_record(session, current_user.id, record_id, data)
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Record not found")


@router.delete("/body-records/{record_id}", status_code=204)
def delete_body_record(
    record_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        record_service.delete_body_record(session, current_user.id, record_id)
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Record not found")
    return None


# Meals
@router.get("/meals", response_model=Pagination[MealRead])
def list_meals(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int | None = Query(None, ge=1, le=100),
    offset: int = Query(0, ge=0),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    meal_type: str | None = Query(None),
):
    return record_service.list_meals(
        session,
        current_user.id,
        limit=limit,
        offset=offset,
        date_from=date_from,
        date_to=date_to,
        meal_type=meal_type,
    )


@router.post("/meals", response_model=MealRead, status_code=201)
def create_meal(
    payload: MealCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = record_service.create_meal(session, current_user.id, payload)
    # Trigger achievement rate calculation
    compute_achievement_rate_task.delay(current_user.id)
    return result


@router.patch("/meals/{meal_id}", response_model=MealRead)
def update_meal(
    meal_id: int,
    payload: MealUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    try:
        return record_service.update_meal(session, current_user.id, meal_id, data)
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Meal not found")


@router.delete("/meals/{meal_id}", status_code=204)
def delete_meal(
    meal_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        record_service.delete_meal(session, current_user.id, meal_id)
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Meal not found")
    return None


# Exercises
@router.get("/exercises", response_model=Pagination[ExerciseRead])
def list_exercises(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int | None = Query(None, ge=1, le=100),
    offset: int = Query(0, ge=0),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
):
    return record_service.list_exercises(
        session,
        current_user.id,
        limit=limit,
        offset=offset,
        date_from=date_from,
        date_to=date_to,
    )


@router.post("/exercises", response_model=ExerciseRead, status_code=201)
def create_exercise(
    payload: ExerciseCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = record_service.create_exercise(session, current_user.id, payload)
    # Trigger achievement rate calculation
    compute_achievement_rate_task.delay(current_user.id)
    return result


@router.patch("/exercises/{exercise_id}", response_model=ExerciseRead)
def update_exercise(
    exercise_id: int,
    payload: ExerciseUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    try:
        return record_service.update_exercise(session, current_user.id, exercise_id, data)
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Exercise not found")


@router.delete("/exercises/{exercise_id}", status_code=204)
def delete_exercise(
    exercise_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        record_service.delete_exercise(session, current_user.id, exercise_id)
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Exercise not found")
    return None


# Diaries
@router.get("/diaries", response_model=Pagination[DiaryRead])
def list_diaries(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int | None = Query(None, ge=1, le=100),
    offset: int = Query(0, ge=0),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
):
    return record_service.list_diaries(
        session,
        current_user.id,
        limit=limit,
        offset=offset,
        date_from=date_from,
        date_to=date_to,
    )


@router.post("/diaries", response_model=DiaryRead, status_code=201)
def create_diary(
    payload: DiaryCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = record_service.create_diary(session, current_user.id, payload)
    # Trigger achievement rate calculation
    compute_achievement_rate_task.delay(current_user.id)
    return result


@router.patch("/diaries/{diary_id}", response_model=DiaryRead)
def update_diary(
    diary_id: int,
    payload: DiaryUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    try:
        return record_service.update_diary(session, current_user.id, diary_id, data)
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Diary not found")


@router.delete("/diaries/{diary_id}", status_code=204)
def delete_diary(
    diary_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        record_service.delete_diary(session, current_user.id, diary_id)
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Diary not found")
    return None


