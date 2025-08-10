from __future__ import annotations

from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.record import BodyRecord, Meal, Exercise, Diary
from app.schemas.enums import MealType


# BodyRecord
def list_body_records_by_user(
    session: Session,
    user_id: int,
    *,
    limit: int | None = None,
    offset: int = 0,
    date_from=None,
    date_to=None,
) -> List[BodyRecord]:
    stmt = select(BodyRecord).where(BodyRecord.user_id == user_id)
    if date_from is not None:
        stmt = stmt.where(BodyRecord.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(BodyRecord.date <= date_to)
    stmt = stmt.order_by(BodyRecord.date.desc()).limit(limit).offset(offset)
    return session.scalars(stmt).all()


def count_body_records_by_user(session: Session, user_id: int, *, date_from=None, date_to=None) -> int:
    stmt = select(func.count()).select_from(BodyRecord).where(BodyRecord.user_id == user_id)
    if date_from is not None:
        stmt = stmt.where(BodyRecord.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(BodyRecord.date <= date_to)
    return session.execute(stmt).scalar_one()


def create_body_record(session: Session, *, user_id: int, data: dict) -> BodyRecord:
    record = BodyRecord(user_id=user_id, **data)
    session.add(record)
    session.flush()
    return record


def get_body_record_by_id(session: Session, user_id: int, record_id: int) -> BodyRecord | None:
    obj = session.get(BodyRecord, record_id)
    return obj if obj and obj.user_id == user_id else None


def update_body_record(session: Session, obj: BodyRecord, data: dict) -> BodyRecord:
    for k, v in data.items():
        setattr(obj, k, v)
    session.flush()
    return obj


def delete_body_record(session: Session, obj: BodyRecord) -> None:
    session.delete(obj)


# Meal
def list_meals_by_user(
    session: Session,
    user_id: int,
    *,
    limit: int | None = None,
    offset: int = 0,
    date_from=None,
    date_to=None,
    meal_type: str | None = None,
) -> List[Meal]:
    stmt = select(Meal).where(Meal.user_id == user_id)
    if date_from is not None:
        stmt = stmt.where(Meal.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(Meal.date <= date_to)
    if meal_type is not None:
        stmt = stmt.where(Meal.meal_type == meal_type)
    stmt = stmt.order_by(Meal.date.desc(), Meal.id.desc()).limit(limit).offset(offset)
    return session.scalars(stmt).all()


def count_meals_by_user(session: Session, user_id: int, *, date_from=None, date_to=None, meal_type: str | None = None) -> int:
    stmt = select(func.count()).select_from(Meal).where(Meal.user_id == user_id)
    if date_from is not None:
        stmt = stmt.where(Meal.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(Meal.date <= date_to)
    if meal_type is not None:
        stmt = stmt.where(Meal.meal_type == meal_type)
    return session.execute(stmt).scalar_one()


def create_meal(session: Session, *, user_id: int, data: dict) -> Meal:
    item = Meal(user_id=user_id, **data)
    session.add(item)
    session.flush()
    return item


def get_meal_by_id(session: Session, user_id: int, meal_id: int) -> Meal | None:
    obj = session.get(Meal, meal_id)
    return obj if obj and obj.user_id == user_id else None


def update_meal(session: Session, obj: Meal, data: dict) -> Meal:
    for k, v in data.items():
        setattr(obj, k, v)
    session.flush()
    return obj


def delete_meal(session: Session, obj: Meal) -> None:
    session.delete(obj)


# Exercise
def list_exercises_by_user(
    session: Session,
    user_id: int,
    *,
    limit: int | None = None,
    offset: int = 0,
    date_from=None,
    date_to=None,
) -> List[Exercise]:
    stmt = select(Exercise).where(Exercise.user_id == user_id)
    if date_from is not None:
        stmt = stmt.where(Exercise.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(Exercise.date <= date_to)
    stmt = stmt.order_by(Exercise.date.desc(), Exercise.id.desc()).limit(limit).offset(offset)
    return session.scalars(stmt).all()


def count_exercises_by_user(session: Session, user_id: int, *, date_from=None, date_to=None) -> int:
    stmt = select(func.count()).select_from(Exercise).where(Exercise.user_id == user_id)
    if date_from is not None:
        stmt = stmt.where(Exercise.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(Exercise.date <= date_to)
    return session.execute(stmt).scalar_one()


def create_exercise(session: Session, *, user_id: int, data: dict) -> Exercise:
    item = Exercise(user_id=user_id, **data)
    session.add(item)
    session.flush()
    return item


def get_exercise_by_id(session: Session, user_id: int, exercise_id: int) -> Exercise | None:
    obj = session.get(Exercise, exercise_id)
    return obj if obj and obj.user_id == user_id else None


def update_exercise(session: Session, obj: Exercise, data: dict) -> Exercise:
    for k, v in data.items():
        setattr(obj, k, v)
    session.flush()
    return obj


def delete_exercise(session: Session, obj: Exercise) -> None:
    session.delete(obj)


# Diary
def list_diaries_by_user(
    session: Session,
    user_id: int,
    *,
    limit: int | None = None,
    offset: int = 0,
    date_from=None,
    date_to=None,
) -> List[Diary]:
    stmt = select(Diary).where(Diary.user_id == user_id)
    if date_from is not None:
        stmt = stmt.where(Diary.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(Diary.date <= date_to)
    stmt = stmt.order_by(Diary.date.desc(), Diary.id.desc()).limit(limit).offset(offset)
    return session.scalars(stmt).all()


def count_diaries_by_user(session: Session, user_id: int, *, date_from=None, date_to=None) -> int:
    stmt = select(func.count()).select_from(Diary).where(Diary.user_id == user_id)
    if date_from is not None:
        stmt = stmt.where(Diary.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(Diary.date <= date_to)
    return session.execute(stmt).scalar_one()


def create_diary(session: Session, *, user_id: int, data: dict) -> Diary:
    item = Diary(user_id=user_id, **data)
    session.add(item)
    session.flush()
    return item


def get_diary_by_id(session: Session, user_id: int, diary_id: int) -> Diary | None:
    obj = session.get(Diary, diary_id)
    return obj if obj and obj.user_id == user_id else None


def update_diary(session: Session, obj: Diary, data: dict) -> Diary:
    for k, v in data.items():
        setattr(obj, k, v)
    session.flush()
    return obj


def delete_diary(session: Session, obj: Diary) -> None:
    session.delete(obj)


def count_record_days_in_range(session: Session, user_id: int, start_date, end_date) -> int:
    # Count distinct dates in any of the record tables for the user within the range
    from sqlalchemy import union
    
    # Get all distinct dates from all record types
    body_dates = select(BodyRecord.date).where(
        BodyRecord.user_id == user_id,
        BodyRecord.date >= start_date,
        BodyRecord.date <= end_date,
    )
    
    meal_dates = select(Meal.date).where(
        Meal.user_id == user_id,
        Meal.date >= start_date,
        Meal.date <= end_date,
    )
    
    exercise_dates = select(Exercise.date).where(
        Exercise.user_id == user_id,
        Exercise.date >= start_date,
        Exercise.date <= end_date,
    )
    
    diary_dates = select(Diary.date).where(
        Diary.user_id == user_id,
        Diary.date >= start_date,
        Diary.date <= end_date,
    )
    
    # Union all dates and count distinct
    all_dates = union(body_dates, meal_dates, exercise_dates, diary_dates).subquery()
    result = session.execute(select(func.count()).select_from(all_dates)).scalar_one()
    return result or 0


