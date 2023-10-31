import asyncio
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from actions import prisma
from settings import FAST_API_CONFIGS, ASGI_CONFIGS
from routers import api


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(**FAST_API_CONFIGS, lifespan=app_lifespan)
    app.include_router(api)
    return app


app = create_app()


async def main() -> None:
    uvicorn.run("main:app", **ASGI_CONFIGS)


if __name__ == "__main__":
    asyncio.run(main())
