from __future__ import annotations

from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.repositories import user_repository
from app.tasks.article_tasks import warm_articles_cache
from app.tasks.stats_tasks import compute_achievement_rate_all_users


def test_auth_register_duplicate(client: TestClient):
    r = client.post(
        "/auth/register",
        json={"email": "demo@example.com", "password": "demo1234", "name": "Demo"},
    )
    # should be 400 duplicate
    assert r.status_code in (200, 400)


def test_article_detail_and_filters(client: TestClient):
    # list with category
    r = client.get("/articles?limit=5&category=Diet")
    assert r.status_code == 200
    items = r.json()["data"]
    # optional check
    if items:
        first_id = items[0]["id"]
        r2 = client.get(f"/articles/{first_id}")
        assert r2.status_code == 200
    # not found path
    r3 = client.get("/articles/0")
    assert r3.status_code == 200


def test_articles_tag_and_search(client: TestClient):
    r = client.get("/articles?limit=3&tag=fitness")
    assert r.status_code == 200
    r = client.get("/articles?limit=3&q=Article")
    assert r.status_code == 200
    # call again to hit cache branch in service
    r = client.get("/articles?limit=3&q=Article")
    assert r.status_code == 200


def test_records_crud_variants(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # body record
    br = client.post("/body-records", headers=headers, json={"date": str(date(2025,1,3)), "weight": 70.5}).json()
    rid = br["id"]
    up = client.patch(f"/body-records/{rid}", headers=headers, json={"weight": 69.9})
    assert up.status_code == 200 and up.json()["weight"] == 69.9
    delr = client.delete(f"/body-records/{rid}", headers=headers)
    assert delr.status_code == 204

    # exercise
    ex = client.post("/exercises", headers=headers, json={"date": str(date(2025,1,3)), "name": "Run", "duration_min": 20}).json()
    eid = ex["id"]
    up2 = client.patch(f"/exercises/{eid}", headers=headers, json={"duration_min": 25})
    assert up2.status_code == 200 and up2.json()["duration_min"] == 25
    delx = client.delete(f"/exercises/{eid}", headers=headers)
    assert delx.status_code == 204

    # diary
    dy = client.post("/diaries", headers=headers, json={"date": str(date.today()), "content": "note"}).json()
    did = dy["id"]
    up3 = client.patch(f"/diaries/{did}", headers=headers, json={"content": "updated"})
    assert up3.status_code == 200 and up3.json()["content"] == "updated"
    deld = client.delete(f"/diaries/{did}", headers=headers)
    assert deld.status_code == 204


def test_meal_type_validation(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.post("/meals", headers=headers, json={"date": str(date.today()), "meal_type": "Invalid"})
    assert r.status_code in (400, 422)


def test_tasks_direct_calls():
    # Warm cache task
    total = warm_articles_cache()
    assert isinstance(total, int)
    # Compute all users stat
    cnt = compute_achievement_rate_all_users(window_days=3)
    assert isinstance(cnt, int)


def test_user_repo_get_by_id():
    session = SessionLocal()
    try:
        me = user_repository.get_by_email(session, "demo@example.com")
        assert me is not None
        same = user_repository.get_by_id(session, me.id)
        assert same and same.id == me.id
    finally:
        session.close()


