from datetime import datetime

from pydantic import BaseModel


class UrlShortenResponse(BaseModel):
    shortened_url: str
    expires_at: datetime