from humps import camelize
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        alias_generator = lambda snake_case: camelize(snake_case)
        populate_by_name = True
