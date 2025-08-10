from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash, create_access_token
from app.repositories import user_repository
from app.models.user import User


def register_user(session: Session, *, email: str, password: str, name: str | None) -> User:
    existing = user_repository.get_by_email(session, email)
    if existing:
        raise ValueError("Email already registered")
    user = user_repository.create(session, email=email, name=name, password_hash=get_password_hash(password))
    return user


def authenticate(session: Session, *, email: str, password: str) -> str:
    user = user_repository.get_by_email(session, email)
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Incorrect email or password")
    return create_access_token(subject=user.id)


