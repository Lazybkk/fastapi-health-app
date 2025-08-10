from __future__ import annotations

from app.tasks.stats_tasks import compute_achievement_rate_task
from app.repositories.user_repository import get_by_email
from app.db.session import SessionLocal


def test_stats_task_inline():
    session = SessionLocal()
    try:
        me = get_by_email(session, "demo@example.com")
        assert me is not None
        # call task directly (not via celery worker) for coverage
        val = compute_achievement_rate_task(me.id, window_days=3)
        assert 0.0 <= val <= 100.0
    finally:
        session.close()


