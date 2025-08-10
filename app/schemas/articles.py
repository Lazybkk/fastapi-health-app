from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict
from app.schemas.enums import ArticleCategory


class TagRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class ArticleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    content: str
    image_url: str | None = None
    category: ArticleCategory
    published_at: datetime | None = None


class ArticleRead(ArticleBase):
    id: int
    tags: List[TagRead] = []


