from __future__ import annotations

from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def get_by_email(session: Session, email: str) -> Optional[User]:
    return session.scalars(select(User).where(User.email == email)).first()


def create(session: Session, *, email: str, name: str | None, password_hash: str) -> User:
    user = User(email=email, name=name, password_hash=password_hash)
    session.add(user)
    session.flush()
    return user


