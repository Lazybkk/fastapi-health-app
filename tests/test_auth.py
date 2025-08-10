from __future__ import annotations

from fastapi.testclient import TestClient


def test_health(client: TestClient):
    r = client.get("/healthz")
    assert r.status_code == 200


def test_login_demo(client: TestClient):
    r = client.post(
        "/auth/login",
        data={"username": "demo@example.com", "password": "demo1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    assert isinstance(token, str) and len(token) > 10

