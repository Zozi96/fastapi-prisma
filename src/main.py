import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from controllers import prisma
from settings import FAST_API_CONFIGS, ASGI_CONFIGS
from routers import url_path_list


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(**FAST_API_CONFIGS)
    for router in url_path_list:
        app.include_router(router["router"], prefix=router["prefix"])
    return app


app = create_app()


async def main() -> None:
    config = uvicorn.Config(app, **ASGI_CONFIGS)
    server = uvicorn.Server(config=config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
