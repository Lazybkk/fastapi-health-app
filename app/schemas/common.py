from __future__ import annotations

from __future__ import annotations

from typing import Generic, List, TypeVar

from pydantic import BaseModel


class PageMeta(BaseModel):
    total: int
    limit: int | None = None
    offset: int = 0


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: List[T]
    meta: PageMeta


class Pagination(BaseModel, Generic[T]):
    data: List[T]
    previous: str
    next: str
    count: int


