from __future__ import annotations

from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.db.session import SessionLocal
from sqlalchemy import text
from app.services.stats_service import compute_achievement_rate


@celery_app.task(name="stats.compute_achievement_rate")
def compute_achievement_rate_task(user_id: int, window_days: int = 30) -> float:
    session: Session = SessionLocal()
    try:
        return compute_achievement_rate(session, user_id=user_id, window_days=window_days)
    finally:
        session.close()


@celery_app.task(name="stats.compute_achievement_rate_all_users")
def compute_achievement_rate_all_users(window_days: int = 30) -> int:
    session: Session = SessionLocal()
    try:
        count = 0
        last_id = 0
        while True:
            users = session.execute(
                text("SELECT id FROM users WHERE id > :last_id ORDER BY id ASC LIMIT 100"),
                {"last_id": last_id},
            ).all()
            if not users:
                break
            for (uid,) in users:
                compute_achievement_rate(session, user_id=uid, window_days=window_days)
                last_id = uid
                count += 1
        return count
    finally:
        session.close()


