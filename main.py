from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from urlshortner.controller.url_controller import router
from urlshortner.repository.pg_pool_processor import PostgresPool


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔄 Startup
    await PostgresPool.init_pool(
        dsn="postgresql://myuser:mypassword@localhost:5431/system-design"
    )
    yield
    # 🔻 Shutdown
    await PostgresPool.close_pool()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

def main():
    uvicorn.run(
        app='main:app',
        host='localhost',
        port=8081
    )


if __name__ == '__main__':
    main()
