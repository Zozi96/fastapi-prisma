from typing import Final, Any

from decouple import config as env


DEBUG: Final[bool] = env("DEBUG", cast=bool, default=False)

FAST_API_CONFIGS: Final[dict[str, Any]] = {
    "title": "Task",
    "description": "This is a project with the purpose of make this app with FastAPI and Prisma",
    "debug": DEBUG
}

ASGI_CONFIGS: Final[dict[str, Any]] = {"port": env("PORT", cast=int), "reload": DEBUG}
