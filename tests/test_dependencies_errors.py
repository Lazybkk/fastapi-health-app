from __future__ import annotations

from fastapi.testclient import TestClient


def test_auth_required_401(client: TestClient):
    r = client.get("/body-records")
    assert r.status_code == 401


