from typing import Final, Any

from decouple import config as env

SECRET_KEY: Final[str] = env("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = env(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=15
)
ALGORITHM: Final[str] = env("ALGORITHM")

DEBUG: Final[bool] = env("DEBUG", cast=bool, default=False)

CORS_CONFIG: Final[dict[str, Any]] = {
    "allow_credentials": True,
    "allow_methods": ("*",),
    "allow_headers": ("*",),
    "allow_origins": (
        "http://localhost:5173",
        "http://localhost",
    ),
}


FAST_API_CONFIGS: Final[dict[str, Any]] = {
    "title": "Task application with FastAPI and Prisma",
    "description": "This is a project with the purpose of make this app with FastAPI and Prisma",
    "debug": DEBUG,
}

ASGI_CONFIGS: Final[dict[str, Any]] = {"port": env("PORT", cast=int), "reload": DEBUG}
