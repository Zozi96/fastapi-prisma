from fastapi import APIRouter, HTTPException, status
from prisma import errors
from prisma.models import Task as TaskRecord
from internal.auth.security import user_logged

from internal.db import Task
from schemas.task import TaskModel, ResponseTaskModel

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[ResponseTaskModel])
async def all_tasks(current_user: user_logged()) -> list[TaskRecord]:
    objects = await Task.find_many(where={"user_id": current_user.id})
    return objects


@router.post("", response_model=ResponseTaskModel)
async def create_task(data: TaskModel, current_user: user_logged()) -> TaskRecord:
    data = data.model_dump()
    data["user_id"] = current_user.id
    obj = await Task.create(data=data)
    return obj


@router.get("/{pk}", response_model=ResponseTaskModel)
async def get_task_by_id(pk: int, current_user: user_logged()) -> TaskRecord:
    try:
        obj = await Task.find_first_or_raise(where={"id": pk})
        return obj
    except errors.RecordNotFoundError:
        raise HTTPException(status_code=status.NOT_FOUND, detail="Item not found")


@router.put("/{pk}", response_model=ResponseTaskModel)
async def edit_task(
    pk: int, data: TaskModel, current_user: user_logged()
) -> TaskRecord:
    obj = await Task.update(where={"id": pk}, data=data.model_dump())
    if not obj:
        raise HTTPException(status_code=status.NOT_FOUND, detail="Item not found")
    return obj
