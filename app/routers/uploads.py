from __future__ import annotations

import secrets
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query

from app.config import settings
from app.dependencies import get_current_user
from app.models.user import User
from app.services.storage import create_presigned_put_s3


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/uploads/presigned", summary="Get S3 presigned POST to upload directly from FE")
def get_presigned_upload(
    current_user: User = Depends(get_current_user),
    content_type: str = Query(..., description="MIME type, e.g. image/jpeg"),
):
    if settings.file_storage != "s3":
        raise HTTPException(status_code=400, detail="S3 storage is not enabled")
    key = f"uploads/{current_user.id}/{secrets.token_hex(8)}"
    presigned = create_presigned_put_s3(key=key, content_type=content_type, expires_in=3600)
    return {"url": presigned.url, "fields": presigned.fields, "public_url": presigned.public_url}


