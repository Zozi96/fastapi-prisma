from fastapi import APIRouter

from routers import home, task


api = APIRouter(prefix="/api")
api.include_router(home.router)
api.include_router(task.router)
