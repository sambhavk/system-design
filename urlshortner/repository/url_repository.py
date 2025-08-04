from typing import Optional
from datetime import datetime

from urlshortner.repository.pg_pool_processor import PostgresPool


class UrlRepository:

    @staticmethod
    async def save_url(original_url: str, shortened_url: str, user_id: Optional[str], expires_at: Optional[datetime]) -> None:
        conn = await PostgresPool.get_connection()
        try:
            await conn.execute("""
                INSERT INTO url_metadata (original_url, shortened_url, user_id, expires_at, created_at)
                VALUES ($1, $2, $3, $4, NOW())
                ON CONFLICT (shortened_url) DO NOTHING;
            """, original_url, shortened_url, user_id, expires_at)
        finally:
            await PostgresPool.release_connection(conn)

    @staticmethod
    async def get_original_url(shortened_url: str) -> Optional[str]:
        conn = await PostgresPool.get_connection()
        try:
            row = await conn.fetchrow("""
                SELECT original_url FROM url_metadata
                WHERE shortened_url = $1 AND (expires_at IS NULL OR expires_at > NOW());
            """, shortened_url)
            return row["original_url"] if row else None
        finally:
            await PostgresPool.release_connection(conn)

    @staticmethod
    async def shortened_url_exists(shortened_url: str) -> bool:
        conn = await PostgresPool.get_connection()
        try:
            row = await conn.fetchrow("""
                SELECT 1 FROM url_metadata WHERE shortened_url = $1;
            """, shortened_url)
            return row is not None
        finally:
            await PostgresPool.release_connection(conn)
