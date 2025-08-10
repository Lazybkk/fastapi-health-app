from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sub: str | None = None
    exp: int | None = None
    iat: int | None = None
    nbf: int | None = None
    # issued_at and not_before as datetimes can be derived if needed


