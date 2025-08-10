from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.security import create_access_token


def test_invalid_bearer_token(client: TestClient):
    r = client.get("/body-records", headers={"Authorization": "Bearer invalid"})
    assert r.status_code == 401


def test_token_with_missing_user(client: TestClient):
    token = create_access_token(subject=99999999)
    r = client.get("/body-records", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


