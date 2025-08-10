from __future__ import annotations

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    name: str | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None


class UserRead(UserBase):
    id: int


