# Heallth App Backend

Backend for a health-tracking web app (coding exercise) with pages: Top, My Record (private), and Column (public).

### Overview
- Provide APIs for body weight/body-fat, meals, exercises, and diaries (private area – JWT)
- Public health articles API with Redis cache and filters by category/tag/search
- Achievement rate calculation and tracking with automatic triggers
- Background jobs via Celery (cache warmup, daily achievement-rate computation), monitored by Flower

### Tech Stack
- FastAPI (Python 3.11), Pydantic v2
- SQLAlchemy 2.x, Alembic (Postgres)
- Redis (cache, Celery broker/backend)
- Celery (worker + beat), Flower (monitor)
- JWT Auth (python-jose), Bcrypt (passlib)
- Docker + docker-compose

### Architecture
- 3-layer: `router` → `service` → `repository`
  - Router: declares endpoints and maps request/response schemas
  - Service: business logic; orchestrates repositories/cache/tasks
  - Repository: database access with SQLAlchemy (Core/ORM)
- Redis caches article lists and achievement rates
- Celery worker for background work; Celery beat for schedules; Flower for monitoring

```
graph TD
  U[Client / Frontend] -->|HTTP| API[FastAPI]
  API -->|SQLAlchemy| PG[(Postgres)]
  API -->|Cache| R[(Redis)]
  API -->|Enqueue| WQ[Celery Queue]
  CB[Celery Beat] --> WQ
  W[Celery Worker] --> PG
  W --> R
  F[Flower] --> WQ
  
  subgraph "Achievement Rate"
    AR[Record Creation] -->|Trigger| WQ
    W -->|Calculate| AR_CALC[Achievement Rate]
    AR_CALC -->|Cache| R
  end
```

### ERD

```
erDiagram
  users ||--o{ body_records : has
  users ||--o{ meals        : has
  users ||--o{ exercises    : has
  users ||--o{ diaries      : has
  users ||--o{ goals        : has
  goals ||--o{ goal_progress : has

  articles o{--o{ tags      : via article_tags

  users {
    int id PK
    string email
    string name
    string password_hash
    datetime created_at
    datetime updated_at
  }

  body_records {
    int id PK
    int user_id FK
    date date
    float weight
    float body_fat_percentage
    datetime created_at
    datetime updated_at
  }

  meals {
    int id PK
    int user_id FK
    date date
    string meal_type
    string image_url
    string description
    int calories
    datetime created_at
    datetime updated_at
  }

  exercises {
    int id PK
    int user_id FK
    date date
    string name
    int duration_min
    int calories
    datetime created_at
    datetime updated_at
  }

  diaries {
    int id PK
    int user_id FK
    date date
    time time
    string content
    datetime created_at
    datetime updated_at
  }

  goals {
    int id PK
    int user_id FK
    string title
    string description
    float target_value
    date target_date
    boolean is_active
    datetime created_at
    datetime updated_at
  }

  goal_progress {
    int id PK
    int goal_id FK
    date date
    float current_value
    boolean is_completed
    string notes
    datetime created_at
    datetime updated_at
  }

  articles {
    int id PK
    string title
    string content
    string image_url
    string category
    datetime published_at
    datetime created_at
    datetime updated_at
  }

  tags {
    int id PK
    string name
  }

  article_tags {
    int article_id FK
    int tag_id FK
  }
```

## Quick Start
```
cp env.example .env
docker compose up -d --build
# Seed demo data
docker compose exec -T web bash -lc 'PYTHONPATH=/app python scripts/seed_data.py'
```

Services:
- API: `http://localhost:8000` (docs: `http://localhost:8000/docs`)
- Flower: `http://localhost:5555` (Celery monitoring)

Demo account:
- email: `demo@example.com`
- password: `demo1234`

## Tests & Coverage
```
docker compose exec -T web bash -lc 'pytest -q'
```
- Minimum coverage 95% (enforced in `pytest.ini`). Celery files are excluded from coverage.

## File storage (local/S3)
- Dynamic by env:
  - `FILE_STORAGE=local|s3`
  - Local (dev):
    - `LOCAL_MEDIA_ROOT=static/uploads`
    - `STATIC_URL_PREFIX=/static/uploads`
    - Static served at `/static/*` (mount in FastAPI/Nginx)
  - S3 (prod):
    - `AWS_REGION`, `AWS_S3_BUCKET`, `AWS_S3_ENDPOINT` (optional for S3-compatible)
    - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`

### Presigned S3 upload
- Endpoint (auth required): `POST /uploads/presigned?content_type=image/jpeg`
- Response:
```json
{
  "url": "https://bucket.s3.amazonaws.com",
  "fields": { "key": "uploads/1/abc123...", "Content-Type": "image/jpeg", "...": "..." },
  "public_url": "https://bucket.s3.amazonaws.com/uploads/1/abc123..."
}
```
- Frontend flow:
  1) Call presigned endpoint, get `url` and `fields`
  2) Build `FormData` with all `fields` + file and POST to `url`
  3) Save `public_url` into `image_url` field when creating/updating records/articles

Example JS:
```js
const presign = await fetch('/uploads/presigned?content_type=' + file.type, { headers: { Authorization: 'Bearer ' + token } }).then(r => r.json());
const fd = new FormData();
Object.entries(presign.fields).forEach(([k, v]) => fd.append(k, v));
fd.append('file', file);
await fetch(presign.url, { method: 'POST', body: fd });
// then submit image_url: presign.public_url to your API
```

## Achievement Rate System

### Calculation
- **Formula**: `(Total Goals Completed / Total Goals Set) × 100%`
- **Window**: Configurable (default: 30 days)
- **Goal types**: User-defined health and fitness goals
- **Cache**: Redis (1 hour TTL)

### APIs
- `GET /stats/achievement-rate` - Current user's achievement rate
- `GET /stats/achievement-rate/user/{user_id}` - Specific user (admin)
- `POST /stats/achievement-rate/trigger` - Manual calculation trigger

### Automatic Triggers
- ✅ When creating new goal progress
- ✅ When updating goal progress
- ✅ When creating new goals

### Background Tasks
- **Daily**: `stats.compute_achievement_rate_all_users` (3:00 AM UTC)
- **On-demand**: `stats.compute_achievement_rate` (per user)
- **Monitor**: Flower dashboard at `http://localhost:5555`

### Example Usage
```bash
# Get current user achievement rate
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/stats/achievement-rate

# Get specific user with custom window
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/stats/achievement-rate/user/1?window_days=7"

# Create a goal
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"title": "Lose 5kg", "target_value": 65.0, "target_date": "2025-09-09"}' \
  http://localhost:8000/records/goals

# Create goal progress (triggers achievement rate calculation)
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"date": "2025-08-11", "current_value": 68.5, "is_completed": true}' \
  http://localhost:8000/records/goals/1/progress

# Trigger calculation for all users
curl -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8000/stats/achievement-rate/trigger
```

## Notes
- DELETE endpoints return 204 No Content on success.
- Alembic autoupgrades on startup; an initial revision is auto-created if missing.
- CORS enabled by default, configurable via `CORS_ORIGINS`.


