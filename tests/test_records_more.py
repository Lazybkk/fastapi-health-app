from __future__ import annotations

from datetime import date
from fastapi.testclient import TestClient


def test_records_filters_and_pagination(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # date filters
    r = client.get(f"/body-records?date_from=2025-01-01&date_to=2025-12-31&limit=1&offset=0", headers=headers)
    assert r.status_code == 200
    r = client.get(f"/meals?meal_type=Lunch&limit=1&offset=0", headers=headers)
    assert r.status_code == 200
    r = client.get(f"/exercises?date_from=2020-01-01&limit=1&offset=0", headers=headers)
    assert r.status_code == 200
    r = client.get(f"/diaries?date_to=2030-01-01&limit=1&offset=0", headers=headers)
    assert r.status_code == 200


