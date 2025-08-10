from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, records
from .routers import articles
from .routers import stats
from .routers import uploads


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, description="Backend for health app test: My Records + Articles + Celery tasks")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(records.router, tags=["records"])  # paths: /body-records, /meals, /exercises, /diaries
    app.include_router(articles.router, tags=["articles"])  # /articles
    app.include_router(stats.router, tags=["stats"])  # /stats
    app.include_router(uploads.router, tags=["uploads"])  # /uploads/presigned

    @app.get("/healthz")
    def healthcheck() -> dict:
        return {"status": "ok"}

    return app


app = create_app()

