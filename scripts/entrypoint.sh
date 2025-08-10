#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH=/app/app

echo "Waiting for Postgres..."
python - <<'PY'
import os, time
import psycopg2
from urllib.parse import urlparse

url = os.environ.get("DATABASE_URL")
if not url:
    raise SystemExit("DATABASE_URL is not set")

parsed = urlparse(url.replace("+psycopg2", ""))
for _ in range(60):
    try:
        conn = psycopg2.connect(
            dbname=parsed.path.lstrip('/'),
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port or 5432,
        )
        conn.close()
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("Postgres not available after waiting")
PY

echo "Running Alembic migrations..."
mkdir -p alembic/versions
alembic upgrade head

echo "Starting API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

