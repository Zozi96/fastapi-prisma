import pydantic as pd


class TaskModel(pd.BaseModel):
    title: pd.constr(min_length=1)
    description: str | None


class ResponseTaskModel(TaskModel):
    id: int
