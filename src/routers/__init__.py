from fastapi import APIRouter

from routers import home, task, user


api = APIRouter(prefix="/api")
api.include_router(home.router)
api.include_router(task.router)
api.include_router(user.router)
