import hashlib
import base64
import random
import string
from datetime import datetime
from typing import Optional

from urlshortner.dto.url_shorten_request import UrlShortenRequest
from urlshortner.repository.url_repository import UrlRepository


class UrlService:

    @staticmethod
    async def shorten_url(data: UrlShortenRequest) -> str:
        # Step 1: Generate a hash of the URL (and user_id to make it unique per user)
        raw = f"{data.original_url}:{data.user_id or ''}:{random.random()}"
        hash_digest = hashlib.sha256(raw.encode()).digest()
        encoded = base64.urlsafe_b64encode(hash_digest).decode()[:8]  # 8-char token

        # Retry on collision (rare if hash is good)
        for _ in range(5):
            exists = await UrlRepository.shortened_url_exists(encoded)
            if not exists:
                break
            encoded = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        else:
            raise Exception("Failed to generate unique short URL")

        # Step 2: Save to DB
        await UrlRepository.save_url(
            original_url=data.original_url.unicode_string(),
            shortened_url=encoded,
            user_id=data.user_id,
            expires_at=data.expires_at,
        )

        return encoded

    @staticmethod
    async def get_original_url(shortened_url: str) -> Optional[str]:
        return await UrlRepository.get_original_url(shortened_url)

    @staticmethod
    async def redirect_url(shortened_url: str) -> Optional[str]:
        """
        You can call this inside a FastAPI route and return RedirectResponse
        """
        original = await UrlService.get_original_url(shortened_url)
        return original  # Or raise custom NotFound exception if None
