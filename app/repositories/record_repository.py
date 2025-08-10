from __future__ import annotations

from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.record import BodyRecord, Meal, Exercise, Diary, Goal, GoalProgress
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


# Goal
def list_goals_by_user(
    session: Session,
    user_id: int,
    *,
    limit: int | None = None,
    offset: int = 0,
    is_active: bool | None = None,
) -> List[Goal]:
    stmt = select(Goal).where(Goal.user_id == user_id)
    if is_active is not None:
        stmt = stmt.where(Goal.is_active == is_active)
    stmt = stmt.order_by(Goal.created_at.desc()).limit(limit).offset(offset)
    return session.scalars(stmt).all()


def count_goals_by_user(session: Session, user_id: int, *, is_active: bool | None = None) -> int:
    stmt = select(func.count()).select_from(Goal).where(Goal.user_id == user_id)
    if is_active is not None:
        stmt = stmt.where(Goal.is_active == is_active)
    return session.execute(stmt).scalar_one()


def create_goal(session: Session, *, user_id: int, data: dict) -> Goal:
    goal = Goal(user_id=user_id, **data)
    session.add(goal)
    session.flush()
    return goal


def get_goal_by_id(session: Session, user_id: int, goal_id: int) -> Goal | None:
    obj = session.get(Goal, goal_id)
    return obj if obj and obj.user_id == user_id else None


def update_goal(session: Session, obj: Goal, data: dict) -> Goal:
    for k, v in data.items():
        setattr(obj, k, v)
    session.flush()
    return obj


def delete_goal(session: Session, obj: Goal) -> None:
    session.delete(obj)


# GoalProgress
def list_goal_progress_by_goal(
    session: Session,
    goal_id: int,
    *,
    limit: int | None = None,
    offset: int = 0,
    date_from=None,
    date_to=None,
) -> List[GoalProgress]:
    stmt = select(GoalProgress).where(GoalProgress.goal_id == goal_id)
    if date_from is not None:
        stmt = stmt.where(GoalProgress.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(GoalProgress.date <= date_to)
    stmt = stmt.order_by(GoalProgress.date.desc()).limit(limit).offset(offset)
    return session.scalars(stmt).all()


def count_goal_progress_by_goal(session: Session, goal_id: int, *, date_from=None, date_to=None) -> int:
    stmt = select(func.count()).select_from(GoalProgress).where(GoalProgress.goal_id == goal_id)
    if date_from is not None:
        stmt = stmt.where(GoalProgress.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(GoalProgress.date <= date_to)
    return session.execute(stmt).scalar_one()


def create_goal_progress(session: Session, *, goal_id: int, data: dict) -> GoalProgress:
    progress = GoalProgress(goal_id=goal_id, **data)
    session.add(progress)
    session.flush()
    return progress


def get_goal_progress_by_id(session: Session, goal_id: int, progress_id: int) -> GoalProgress | None:
    obj = session.get(GoalProgress, progress_id)
    return obj if obj and obj.goal_id == goal_id else None


def update_goal_progress(session: Session, obj: GoalProgress, data: dict) -> GoalProgress:
    for k, v in data.items():
        setattr(obj, k, v)
    session.flush()
    return obj


def delete_goal_progress(session: Session, obj: GoalProgress) -> None:
    session.delete(obj)


def count_completed_goals_by_user(session: Session, user_id: int, *, date_from=None, date_to=None) -> int:
    """Count distinct goals that have been completed within a date range"""
    stmt = select(func.count(func.distinct(Goal.id))).select_from(GoalProgress).join(Goal).where(
        Goal.user_id == user_id,
        GoalProgress.is_completed == True
    )
    if date_from is not None:
        stmt = stmt.where(GoalProgress.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(GoalProgress.date <= date_to)
    return session.execute(stmt).scalar_one()


def count_total_goals_by_user(session: Session, user_id: int) -> int:
    """Count total active goals for a user"""
    stmt = select(func.count()).select_from(Goal).where(
        Goal.user_id == user_id,
        Goal.is_active == True
    )
    return session.execute(stmt).scalar_one()


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


