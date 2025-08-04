from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field


def default_expires_at() -> datetime:
    return datetime.now() + timedelta(days=365 * 100)

class UrlShortenRequest(BaseModel):
    original_url: HttpUrl
    expires_at: Optional[datetime] = Field(default_factory=default_expires_at)
    user_id: Optional[UUID]
