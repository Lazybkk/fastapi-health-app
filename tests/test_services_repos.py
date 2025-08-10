from __future__ import annotations

from datetime import date

from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.repositories import user_repository, record_repository
from app.services import auth_service, record_service, stats_service


def test_auth_service_register_and_auth():
    session = SessionLocal()
    try:
        u = auth_service.register_user(session, email="svc_user@example.com", password="x1234567", name="Svc")
        assert u.id is not None
        token = auth_service.authenticate(session, email="svc_user@example.com", password="x1234567")
        assert isinstance(token, str)
    finally:
        session.close()


def test_record_repo_and_service_flow(client: TestClient, auth_token: str):
    session = SessionLocal()
    try:
        me = user_repository.get_by_email(session, "demo@example.com")
        assert me is not None
        # create
        created = record_service.create_body_record(
            session,
            me.id,
            payload=type("obj", (), {"model_dump": lambda self=None: {"date": date(2025, 1, 2), "weight": 72.1, "body_fat_percentage": 20.5}})(),
        )
        assert created.weight == 72.1

        # list
        page = record_service.list_body_records(session, me.id, limit=5)
        assert hasattr(page, "data") and hasattr(page, "count")

        # update
        updated = record_service.update_body_record(session, me.id, record_id=created.id, data={"weight": 71.8})
        assert updated.weight == 71.8

        # delete
        record_service.delete_body_record(session, me.id, record_id=created.id)
    finally:
        session.close()


def test_stats_service_compute_cached():
    session = SessionLocal()
    try:
        me = user_repository.get_by_email(session, "demo@example.com")
        assert me is not None
        rate = stats_service.compute_achievement_rate(session, me.id, window_days=7)
        assert 0.0 <= rate <= 100.0
        cached = stats_service.get_cached_achievement_rate(me.id)
        assert cached and "value" in cached
    finally:
        session.close()


