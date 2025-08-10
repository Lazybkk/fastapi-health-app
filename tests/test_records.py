from __future__ import annotations

from fastapi.testclient import TestClient


def test_list_body_records(client: TestClient, auth_token: str):
    r = client.get("/body-records?limit=2", headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "data" in data and isinstance(data["data"], list)
    assert "count" in data and "previous" in data and "next" in data


def test_create_update_delete_meal(client: TestClient, auth_token: str):
    payload = {
        "date": "2025-01-01",
        "meal_type": "Lunch",
        "description": "Test meal",
        "calories": 500,
    }
    r = client.post("/meals", headers={"Authorization": f"Bearer {auth_token}"}, json=payload)
    assert r.status_code == 201, r.text
    meal_id = r.json()["id"]

    r = client.patch(f"/meals/{meal_id}", headers={"Authorization": f"Bearer {auth_token}"}, json={"description": "Updated"})
    assert r.status_code == 200
    assert r.json()["description"] == "Updated"

    r = client.delete(f"/meals/{meal_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 204

