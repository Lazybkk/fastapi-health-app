from __future__ import annotations

from celery import Celery
from celery.schedules import crontab
from app.config import settings


celery_app = Celery(
    "heallth_app",
    broker=settings.redis_url,
    backend=settings.redis_url,
)


@celery_app.task
def ping() -> str:
    return "pong"


# Celery Beat schedule
celery_app.conf.timezone = "UTC"
celery_app.conf.beat_schedule = {
    "warm-articles-cache": {
        "task": "articles.warm_articles_cache",
        "schedule": crontab(minute="*/15"),
    },
    "compute-achievement-rate-daily": {
        "task": "stats.compute_achievement_rate_all_users",
        "schedule": crontab(minute=0, hour=3),
    },
}


