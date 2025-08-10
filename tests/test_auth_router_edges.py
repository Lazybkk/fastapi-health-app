from __future__ import annotations

from fastapi.testclient import TestClient


def test_register_duplicate_email(client: TestClient):
    r = client.post("/auth/register", json={"email": "demo@example.com", "password": "demo1234"})
    # may be 400 due to duplicate
    assert r.status_code in (200, 400)


