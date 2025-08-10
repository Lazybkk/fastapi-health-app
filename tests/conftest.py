from __future__ import annotations

import os
import sys
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("TESTING", "1")
# Ensure /app is on PYTHONPATH when running inside container
if "/app" not in sys.path:
    sys.path.insert(0, "/app")


@pytest.fixture(scope="session")
def client() -> TestClient:
    from app.main import app
    return TestClient(app)


@pytest.fixture()
def auth_token(client: TestClient) -> str:
    r = client.post(
        "/auth/login",
        data={"username": "demo@example.com", "password": "demo1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


