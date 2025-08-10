from __future__ import annotations

from app.db.session import SessionLocal
from app.repositories import article_repository


def test_article_repository_branches():
    session = SessionLocal()
    try:
        # basic list
        articles = article_repository.list_articles(session, category=None, tag=None, q=None, limit=5, offset=0)
        assert isinstance(articles, list)

        # list with category and q
        _ = article_repository.list_articles(session, category="Diet", tag=None, q="Article", limit=3, offset=0)

        # list with tag
        _ = article_repository.list_articles(session, category=None, tag="fitness", q=None, limit=3, offset=0)

        # get article and tags
        if articles:
            a = articles[0]
            _ = article_repository.get_article(session, a.id)
            _ = article_repository.list_tags_by_article(session, a.id)

            # tag mapping for multiple ids
            _ = article_repository.list_tags_for_articles(session, [a.id])
    finally:
        session.close()


