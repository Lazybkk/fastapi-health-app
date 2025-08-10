from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import boto3

from app.config import settings


@dataclass
class PresignedPut:
    url: str
    fields: dict
    public_url: str


def create_presigned_put_s3(key: str, content_type: str, expires_in: int = 3600) -> PresignedPut:
    if not settings.aws_s3_bucket:
        raise RuntimeError("AWS_S3_BUCKET is not configured")
    session = boto3.session.Session(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
    )
    s3 = session.client("s3", endpoint_url=settings.aws_s3_endpoint)

    presigned = s3.generate_presigned_post(
        Bucket=settings.aws_s3_bucket,
        Key=key,
        Fields={"Content-Type": content_type, "acl": "public-read"},
        Conditions=[["starts-with", "$Content-Type", ""], {"acl": "public-read"}],
        ExpiresIn=expires_in,
    )

    # Build public URL (works for AWS and most S3-compatible endpoints)
    base = settings.aws_s3_endpoint or f"https://{settings.aws_s3_bucket}.s3.amazonaws.com"
    public_url = f"{base}/{key}"
    return PresignedPut(url=presigned["url"], fields=presigned["fields"], public_url=public_url)



