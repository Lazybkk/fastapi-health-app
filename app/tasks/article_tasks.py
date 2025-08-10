from __future__ import annotations

from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.db.session import SessionLocal
from app.services.article_service import list_articles


@celery_app.task(name="articles.warm_articles_cache")
def warm_articles_cache() -> int:
    session: Session = SessionLocal()
    try:
        # Warm a few common combinations
        combos = [
            {"category": None, "tag": None, "q": None, "limit": 10, "offset": 0},
            {"category": "Diet", "tag": None, "q": None, "limit": 10, "offset": 0},
            {"category": "Beauty", "tag": None, "q": None, "limit": 10, "offset": 0},
            {"category": "Health", "tag": None, "q": None, "limit": 10, "offset": 0},
        ]
        total = 0
        for c in combos:
            page = list_articles(session, **c)
            total += page.count if hasattr(page, "count") else 0
        return total
    finally:
        session.close()


