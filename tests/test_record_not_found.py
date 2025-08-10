from __future__ import annotations

from fastapi.testclient import TestClient


def test_update_delete_not_found(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.patch("/body-records/999999", headers=headers, json={"weight": 1})
    assert r.status_code == 404
    r = client.delete("/body-records/999999", headers=headers)
    assert r.status_code == 404
    r = client.patch("/meals/999999", headers=headers, json={"description": "x"})
    assert r.status_code == 404
    r = client.delete("/meals/999999", headers=headers)
    assert r.status_code == 404
    r = client.patch("/exercises/999999", headers=headers, json={"duration_min": 1})
    assert r.status_code == 404
    r = client.delete("/exercises/999999", headers=headers)
    assert r.status_code == 404
    r = client.patch("/diaries/999999", headers=headers, json={"content": "x"})
    assert r.status_code == 404
    r = client.delete("/diaries/999999", headers=headers)
    assert r.status_code == 404

