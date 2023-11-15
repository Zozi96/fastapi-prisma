from datetime import datetime
from internal import BaseSchema

import pydantic as pd


class TaskModel(BaseSchema):
    title: pd.constr(min_length=1)
    description: str | None


class ResponseTaskModel(TaskModel):
    id: int
    created_at: datetime
    updated_at: datetime

    @pd.field_serializer("created_at")
    def serialize_created_at(self, v: datetime, _info) -> str:
        return v.strftime("%Y-%m-%d %H:%M:%S")

    @pd.field_serializer("updated_at")
    def serialize_updated_at(self, v: datetime, _info) -> str:
        return v.strftime("%Y-%m-%d %H:%M:%S")
