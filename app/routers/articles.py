from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.articles import ArticleRead
from app.schemas.enums import ArticleCategory
from app.schemas.common import Pagination
from app.services import article_service


router = APIRouter()


@router.get("/articles", response_model=Pagination[ArticleRead])
def list_articles(
    session: Session = Depends(get_db),
    category: str | None = Query(None),
    tag: str | None = Query(None),
    q: str | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    return article_service.list_articles(
        session,
        category=category,
        tag=tag,
        q=q,
        limit=limit,
        offset=offset,
    )


@router.get("/articles/{article_id}", response_model=ArticleRead)
def get_article(article_id: int, session: Session = Depends(get_db)):
    result = article_service.get_article(session, article_id)
    if result is None:
        return ArticleRead(id=0, title="", content="", image_url=None, category=ArticleCategory.Recommended, published_at=None, tags=[])
    return result


