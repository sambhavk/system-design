from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, field_validator


class UrlMetadata(BaseModel):
    id: Optional[int] = None
    original_url: HttpUrl
    shortened_url: str
    user_id: Optional[UUID] = None
    expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    @field_validator('shortened_url')
    def validate_shortened_url(self, value):
        if not value.isalnum():
            raise ValueError("Shortened URL must be alphanumeric")
        if not (1 <= len(value) <= 7):
            raise ValueError("Length must be between 1 and 7 characters")
        return value

    @field_validator('expires_at')
    def validate_expiry(self, value):
        if value <= datetime.now():
            raise ValueError("expires_at must be in the future")
        return value