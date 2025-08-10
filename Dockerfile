FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (for psycopg2-binary minimal, but ensure build tools available)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl bash \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic
COPY scripts ./scripts

RUN chmod +x scripts/entrypoint.sh

EXPOSE 8000

CMD ["bash", "/app/scripts/entrypoint.sh"]

