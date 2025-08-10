from __future__ import annotations

from typing import List
from sqlalchemy.orm import Session

from app.repositories import article_repository
from app.schemas.articles import ArticleRead, TagRead
from app.schemas.common import Pagination
from app.services.cache import cache_get, cache_set


def list_articles(
    session: Session,
    *,
    category: str | None,
    tag: str | None,
    q: str | None,
    limit: int,
    offset: int,
) -> List[ArticleRead] | Pagination[ArticleRead]:
    cache_key = f"articles:list:{category}:{tag}:{q}:{limit}:{offset}"
    cached = cache_get(cache_key)
    if cached is not None:
        # cached payload is the pagination shape
        return Pagination[ArticleRead](**cached)  # type: ignore[arg-type]

    articles = article_repository.list_articles(
        session,
        category=category,
        tag=tag,
        q=q,
        limit=limit,
        offset=offset,
    )
    results: list[ArticleRead] = []
    if articles:
        article_ids = [a.id for a in articles]
        tag_rows = article_repository.list_tags_for_articles(session, article_ids)
        map_tags: dict[int, list[TagRead]] = {}
        for article_id, tag_obj in tag_rows:
            map_tags.setdefault(article_id, []).append(TagRead.model_validate(tag_obj))
        for a in articles:
            results.append(
                ArticleRead(
                    id=a.id,
                    title=a.title,
                    content=a.content,
                    image_url=a.image_url,
                    category=a.category,
                    published_at=a.published_at,
                    tags=map_tags.get(a.id, []),
                )
            )

    total = article_repository.count_articles(session, category=category, tag=tag, q=q)
    # Build prev/next as simple placeholders; can compute properly if needed
    prev_offset = max(0, (offset or 0) - (limit or 0 or 10))
    next_offset = (offset or 0) + (limit or 0 or 10)
    previous = ""
    next_ = ""
    if offset and offset > 0:
        previous = f"?limit={limit or 10}&offset={prev_offset}"
    if next_offset < total:
        next_ = f"?limit={limit or 10}&offset={next_offset}"

    payload = {
        "data": [r.model_dump() for r in results],
        "previous": previous,
        "next": next_,
        "count": total,
    }
    cache_set(cache_key, payload, ttl_seconds=60)
    return Pagination[ArticleRead](**payload)  # type: ignore[arg-type]


def get_article(session: Session, article_id: int) -> ArticleRead | None:
    a = article_repository.get_article(session, article_id)
    if not a:
        return None
    tags = [TagRead.model_validate(t) for t in article_repository.list_tags_by_article(session, article_id)]
    return ArticleRead(
        id=a.id,
        title=a.title,
        content=a.content,
        image_url=a.image_url,
        category=a.category,
        published_at=a.published_at,
        tags=tags,
    )


