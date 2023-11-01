import pydantic as pd

from internal.db import User


class UserBase(pd.BaseModel):
    email: pd.EmailStr


class UserForm(UserBase):
    password: str = pd.Field(min_length=8, max_length=32)


class UserResponse(UserBase):
    id: int
