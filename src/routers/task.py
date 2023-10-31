from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from prisma import errors

from controllers import Task
from schemas.task import TaskModel, ResponseTaskModel

router = APIRouter(prefix="/tasks")


@router.get("/all", response_model=list[TaskModel])
async def all_tasks():
    objects = await Task.find_many()
    return objects


@router.post("/create", response_model=ResponseTaskModel)
async def create_task(data: TaskModel):
    obj = await Task.create(data=data.model_dump())
    return obj


@router.get("/{pk}")
async def get_task_by_id(pk: int):
    try:
        obj = await Task.find_first_or_raise(where={"id": pk})
        return obj
    except errors.RecordNotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")


@router.put("/edit/{pk}", response_model=ResponseTaskModel)
async def edit_task(pk: int, data: TaskModel):
    obj = await Task.update(where={"id": pk}, data=data.model_dump())
    if not obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    return obj
