from __future__ import annotations

from datetime import date
from fastapi.testclient import TestClient


def test_records_router_missing_fields(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # missing weight should 422
    r = client.post("/body-records", headers=headers, json={"date": str(date.today())})
    assert r.status_code in (400, 422)


