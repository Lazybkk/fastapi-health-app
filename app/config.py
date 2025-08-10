import os
from datetime import timedelta


class Settings:
    app_name: str = os.getenv("APP_NAME", "heallth_app")
    app_env: str = os.getenv("APP_ENV", "development")

    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    secret_key: str = os.getenv("SECRET_KEY", "change_me")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # CORS
    _cors_env = os.getenv("CORS_ORIGINS", "*")
    cors_origins: list[str] = [o.strip() for o in _cors_env.split(",") if o.strip()]

    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.access_token_expire_minutes)

    # Storage config
    file_storage: str = os.getenv("FILE_STORAGE", "local")  # local | s3
    local_media_root: str = os.getenv("LOCAL_MEDIA_ROOT", "static/uploads")
    static_url_prefix: str = os.getenv("STATIC_URL_PREFIX", "/static/uploads")
    aws_region: str | None = os.getenv("AWS_REGION")
    aws_s3_bucket: str | None = os.getenv("AWS_S3_BUCKET")
    aws_s3_endpoint: str | None = os.getenv("AWS_S3_ENDPOINT")
    aws_access_key_id: str | None = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")


settings = Settings()

