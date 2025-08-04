from typing import Optional

import asyncpg


class PostgresPool:
    _pool: Optional[asyncpg.pool.Pool] = None

    @classmethod
    async def init_pool(cls, dsn: str, min_size: int = 5, max_size: int = 20):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                dsn=dsn,
                min_size=min_size,
                max_size=max_size,
                timeout=10,
            )
            print("✅ Postgres pool initialized")
        else:
            print("⚠️ Postgres pool already initialized")

    @classmethod
    async def get_connection(cls):
        if cls._pool is None:
            raise RuntimeError("Postgres pool not initialized. Call `init_pool()` first.")
        return await cls._pool.acquire()

    @classmethod
    async def release_connection(cls, conn):
        if cls._pool:
            await cls._pool.release(conn)

    @classmethod
    async def close_pool(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
            print("🚫 Postgres pool closed")
