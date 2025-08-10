from __future__ import annotations

from fastapi.testclient import TestClient


def test_auth_me(client: TestClient, auth_token: str):
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "demo@example.com"


