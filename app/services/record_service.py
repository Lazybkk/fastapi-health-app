from __future__ import annotations

from typing import List, Tuple
from sqlalchemy.orm import Session

from app.repositories import record_repository
from app.schemas.common import Page, PageMeta, Pagination
from app.schemas.records import (
    BodyRecordCreate,
    BodyRecordRead,
    MealCreate,
    MealRead,
    ExerciseCreate,
    ExerciseRead,
    DiaryCreate,
    DiaryRead,
)


def list_body_records(
    session: Session,
    user_id: int,
    *,
    limit: int | None = None,
    offset: int = 0,
    date_from=None,
    date_to=None,
) -> Page:
    records = record_repository.list_body_records_by_user(
        session, user_id, limit=limit, offset=offset, date_from=date_from, date_to=date_to
    )
    total = record_repository.count_body_records_by_user(session, user_id, date_from=date_from, date_to=date_to)
    return Pagination(
        data=[BodyRecordRead.model_validate(r) for r in records],
        previous="",
        next="",
        count=total,
    )


def create_body_record(session: Session, user_id: int, payload: BodyRecordCreate) -> BodyRecordRead:
    record = record_repository.create_body_record(session, user_id=user_id, data=payload.model_dump())
    return BodyRecordRead.model_validate(record)


def list_meals(
    session: Session,
    user_id: int,
    *,
    limit: int | None = None,
    offset: int = 0,
    date_from=None,
    date_to=None,
    meal_type: str | None = None,
) -> Page:
    items = record_repository.list_meals_by_user(
        session, user_id, limit=limit, offset=offset, date_from=date_from, date_to=date_to, meal_type=meal_type
    )
    total = record_repository.count_meals_by_user(session, user_id, date_from=date_from, date_to=date_to, meal_type=meal_type)
    return Pagination(
        data=[MealRead.model_validate(i) for i in items],
        previous="",
        next="",
        count=total,
    )


def create_meal(session: Session, user_id: int, payload: MealCreate) -> MealRead:
    item = record_repository.create_meal(session, user_id=user_id, data=payload.model_dump())
    return MealRead.model_validate(item)


def list_exercises(
    session: Session,
    user_id: int,
    *,
    limit: int | None = None,
    offset: int = 0,
    date_from=None,
    date_to=None,
) -> Page:
    items = record_repository.list_exercises_by_user(
        session, user_id, limit=limit, offset=offset, date_from=date_from, date_to=date_to
    )
    total = record_repository.count_exercises_by_user(session, user_id, date_from=date_from, date_to=date_to)
    return Pagination(
        data=[ExerciseRead.model_validate(i) for i in items],
        previous="",
        next="",
        count=total,
    )


def create_exercise(session: Session, user_id: int, payload: ExerciseCreate) -> ExerciseRead:
    item = record_repository.create_exercise(session, user_id=user_id, data=payload.model_dump())
    return ExerciseRead.model_validate(item)


def list_diaries(
    session: Session,
    user_id: int,
    *,
    limit: int | None = None,
    offset: int = 0,
    date_from=None,
    date_to=None,
) -> Page:
    items = record_repository.list_diaries_by_user(
        session, user_id, limit=limit, offset=offset, date_from=date_from, date_to=date_to
    )
    total = record_repository.count_diaries_by_user(session, user_id, date_from=date_from, date_to=date_to)
    return Pagination(
        data=[DiaryRead.model_validate(i) for i in items],
        previous="",
        next="",
        count=total,
    )


def update_body_record(session: Session, user_id: int, record_id: int, data: dict) -> BodyRecordRead:
    obj = record_repository.get_body_record_by_id(session, user_id, record_id)
    if obj is None:
        raise ValueError("Record not found")
    obj = record_repository.update_body_record(session, obj, data)
    return BodyRecordRead.model_validate(obj)


def delete_body_record(session: Session, user_id: int, record_id: int) -> None:
    obj = record_repository.get_body_record_by_id(session, user_id, record_id)
    if obj is None:
        raise ValueError("Record not found")
    record_repository.delete_body_record(session, obj)


def update_meal(session: Session, user_id: int, meal_id: int, data: dict) -> MealRead:
    obj = record_repository.get_meal_by_id(session, user_id, meal_id)
    if obj is None:
        raise ValueError("Meal not found")
    obj = record_repository.update_meal(session, obj, data)
    return MealRead.model_validate(obj)


def delete_meal(session: Session, user_id: int, meal_id: int) -> None:
    obj = record_repository.get_meal_by_id(session, user_id, meal_id)
    if obj is None:
        raise ValueError("Meal not found")
    record_repository.delete_meal(session, obj)


def update_exercise(session: Session, user_id: int, exercise_id: int, data: dict) -> ExerciseRead:
    obj = record_repository.get_exercise_by_id(session, user_id, exercise_id)
    if obj is None:
        raise ValueError("Exercise not found")
    obj = record_repository.update_exercise(session, obj, data)
    return ExerciseRead.model_validate(obj)


def delete_exercise(session: Session, user_id: int, exercise_id: int) -> None:
    obj = record_repository.get_exercise_by_id(session, user_id, exercise_id)
    if obj is None:
        raise ValueError("Exercise not found")
    record_repository.delete_exercise(session, obj)


def update_diary(session: Session, user_id: int, diary_id: int, data: dict) -> DiaryRead:
    obj = record_repository.get_diary_by_id(session, user_id, diary_id)
    if obj is None:
        raise ValueError("Diary not found")
    obj = record_repository.update_diary(session, obj, data)
    return DiaryRead.model_validate(obj)


def delete_diary(session: Session, user_id: int, diary_id: int) -> None:
    obj = record_repository.get_diary_by_id(session, user_id, diary_id)
    if obj is None:
        raise ValueError("Diary not found")
    record_repository.delete_diary(session, obj)


def create_diary(session: Session, user_id: int, payload: DiaryCreate) -> DiaryRead:
    item = record_repository.create_diary(session, user_id=user_id, data=payload.model_dump())
    return DiaryRead.model_validate(item)


