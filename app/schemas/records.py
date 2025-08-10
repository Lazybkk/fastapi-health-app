from __future__ import annotations

from datetime import date, time
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


class BodyRecordRead(BodyRecordBase):
    id: int


class BodyRecordUpdate(BaseModel):
    date: Optional[date] = None
    weight: Optional[float] = None
    body_fat_percentage: Optional[float] = None


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
            raise ValueError(f"meal_type must be one of {sorted(allowed)}")
        return v


class MealCreate(MealBase):
    pass


class MealRead(MealBase):
    id: int


class MealUpdate(BaseModel):
    date: Optional[date] = None
    meal_type: Optional[MealType] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    calories: Optional[int] = None

    @field_validator("meal_type")
    @classmethod
    def validate_meal_type(cls, v: Optional[MealType]) -> Optional[MealType]:
        if v is None:
            return v
        allowed = {MealType.Morning, MealType.Lunch, MealType.Dinner, MealType.Snack}
        if v not in allowed:
            raise ValueError(f"meal_type must be one of {[m.value for m in sorted(allowed, key=lambda x: x.value)]}")
        return v


class ExerciseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    name: str
    duration_min: int
    calories: int | None = None


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseRead(ExerciseBase):
    id: int


class ExerciseUpdate(BaseModel):
    date: Optional[date] = None
    name: Optional[str] = None
    duration_min: Optional[int] = None
    calories: Optional[int] = None


class DiaryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    time: Optional[time] = None
    content: str


class DiaryCreate(DiaryBase):
    pass


class DiaryRead(DiaryBase):
    id: int


class DiaryUpdate(BaseModel):
    date: Optional[date] = None
    time: Optional[time] = None
    content: Optional[str] = None


