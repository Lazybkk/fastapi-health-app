from __future__ import annotations

from fastapi.testclient import TestClient


def test_articles_list_public(client: TestClient):
    r = client.get("/articles?limit=3")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data and isinstance(data["data"], list)


def test_stats_enqueue_and_get(client: TestClient, auth_token: str):
    r = client.post("/stats/achievement-rate/enqueue", headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 200
    r = client.get("/stats/achievement-rate", headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 200

