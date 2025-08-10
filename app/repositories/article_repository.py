from __future__ import annotations

from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.article import Article, Tag, ArticleTag


def list_articles(
    session: Session,
    *,
    category: str | None,
    tag: str | None,
    q: str | None,
    limit: int,
    offset: int,
) -> List[Article]:
    stmt = select(Article)
    if category:
        stmt = stmt.where(Article.category == category)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(func.lower(Article.title).like(func.lower(like)))
    if tag:
        stmt = (
            select(Article)
            .join(ArticleTag, ArticleTag.article_id == Article.id)
            .join(Tag, Tag.id == ArticleTag.tag_id)
            .where(Tag.name == tag)
        )
        if category:
            stmt = stmt.where(Article.category == category)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(func.lower(Article.title).like(func.lower(like)))

    stmt = stmt.order_by(Article.published_at.desc().nullslast(), Article.id.desc()).limit(limit).offset(offset)
    return session.scalars(stmt).all()


def count_articles(
    session: Session,
    *,
    category: str | None,
    tag: str | None,
    q: str | None,
) -> int:
    if tag:
        stmt = (
            select(func.count())
            .select_from(Article)
            .join(ArticleTag, ArticleTag.article_id == Article.id)
            .join(Tag, Tag.id == ArticleTag.tag_id)
            .where(Tag.name == tag)
        )
    else:
        stmt = select(func.count()).select_from(Article)
    if category:
        stmt = stmt.where(Article.category == category)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(func.lower(Article.title).like(func.lower(like)))
    return session.execute(stmt).scalar_one()


def list_tags_for_articles(session: Session, article_ids: list[int]) -> list[tuple[int, Tag]]:
    return session.execute(
        select(ArticleTag.article_id, Tag).join(Tag, Tag.id == ArticleTag.tag_id).where(ArticleTag.article_id.in_(article_ids))
    ).all()


def get_article(session: Session, article_id: int) -> Article | None:
    return session.get(Article, article_id)


def list_tags_by_article(session: Session, article_id: int) -> list[Tag]:
    return (
        session.execute(select(Tag).join(ArticleTag, ArticleTag.tag_id == Tag.id).where(ArticleTag.article_id == article_id))
        .scalars()
        .all()
    )


