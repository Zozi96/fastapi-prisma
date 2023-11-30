import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn

from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware

from internal.db import prisma
from internal.settings import FAST_API_CONFIGS, ASGI_CONFIGS, CORS_CONFIG
from internal.auth.router import api as api_auth
from routers import api


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    A coroutine that connects to the Prisma ORM when the FastAPI app starts up,
    and disconnects from it when the app shuts down.

    Args:
        app (FastAPI): The FastAPI app instance.

    Yields:
        None: This coroutine does not return anything.
    """
    await prisma.connect()
    yield
    await prisma.disconnect()


def create_app() -> FastAPI:
    """
    Creates a new FastAPI instance with the specified configurations and routers.

    Returns:
        FastAPI: The newly created FastAPI instance.
    """
    application = FastAPI(**FAST_API_CONFIGS, lifespan=app_lifespan)
    application.add_middleware(CORSMiddleware, **CORS_CONFIG)
    application.include_router(api_auth)
    application.include_router(api)
    return application


app = create_app()


@app.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")


async def main() -> None:
    """Runs the FastAPI application using Uvicorn server with ASGI configurations."""
    uvicorn.run("main:app", **ASGI_CONFIGS)


if __name__ == "__main__":
    asyncio.run(main())
