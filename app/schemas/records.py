from __future__ import annotations

from datetime import date, time, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator
from app.schemas.enums import MealType


class BodyRecordBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    weight: float
    body_fat_percentage: Optional[float] = None


class BodyRecordCreate(BodyRecordBase):
    pass


class BodyRecordUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: Optional[date] = None
    weight: Optional[float] = None
    body_fat_percentage: Optional[float] = None


class BodyRecordRead(BodyRecordBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str


class GoalBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: Optional[str] = None
    target_value: Optional[float] = None
    target_date: Optional[date] = None
    is_active: bool = True


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None
    description: Optional[str] = None
    target_value: Optional[float] = None
    target_date: Optional[date] = None
    is_active: Optional[bool] = None


class GoalRead(GoalBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class GoalProgressBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    goal_id: int
    date: date
    current_value: Optional[float] = None
    is_completed: bool = False
    notes: Optional[str] = None


class GoalProgressCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    current_value: Optional[float] = None
    is_completed: bool = False
    notes: Optional[str] = None


class GoalProgressUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: Optional[date] = None
    current_value: Optional[float] = None
    is_completed: Optional[bool] = None
    notes: Optional[str] = None


class GoalProgressRead(GoalProgressBase):
    id: int
    created_at: datetime
    updated_at: datetime


class MealBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    meal_type: MealType
    image_url: Optional[str] = None
    description: Optional[str] = None
    calories: Optional[int] = None

    @field_validator("meal_type")
    @classmethod
    def validate_meal_type_base(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed = {"Morning", "Lunch", "Dinner", "Snack"}
        if v not in allowed:
            raise ValueError(f"meal_type must be one of {[m.value for m in sorted(allowed, key=lambda x: x.value)]}")
        return v


class MealCreate(MealBase):
    pass


class MealUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: Optional[date] = None
    meal_type: Optional[MealType] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    calories: Optional[int] = None


class MealRead(MealBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str


class ExerciseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    name: str
    duration_min: int
    calories: Optional[int] = None


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: Optional[date] = None
    name: Optional[str] = None
    duration_min: Optional[int] = None
    calories: Optional[int] = None


class ExerciseRead(ExerciseBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str


class DiaryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    time: Optional[time] = None
    content: str


class DiaryCreate(DiaryBase):
    pass


class DiaryUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: Optional[date] = None
    time: Optional[time] = None
    content: Optional[str] = None


class DiaryRead(DiaryBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str


