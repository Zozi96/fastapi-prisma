from datetime import datetime
from typing import Self
import pydantic as pd
from internal import BaseSchema


class UserBase(BaseSchema):
    email: pd.EmailStr = pd.Field(examples=["john.doe@mail.com"])
    first_name: str | None = pd.Field(default="", max_length=100, examples=["John"])
    last_name: str | None = pd.Field(default="", max_length=100, examples=["Doe"])


class UserForm(UserBase):
    password: str = pd.Field(min_length=8, max_length=32, examples=["mysecretpassword"])


class UserChangePassword(BaseSchema):
    old_password: str = pd.Field(
        min_length=6, max_length=32, examples=["mysecretoldpassword"]
    )
    new_password: str = pd.Field(
        min_length=6, max_length=32, examples=["mysecretnewpassword"]
    )

    @pd.model_validator(mode="after")
    def check_passwords_match(cls, obj: Self) -> Self:
        old_password, new_password = obj.old_password, obj.new_password
        if old_password == new_password:
            raise pd.ValidationError("New password must be different from old password")
        return obj


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @pd.field_serializer("created_at")
    def serialize_created_at(self, v: datetime, _info) -> str:
        return v.strftime("%Y-%m-%d %H:%M:%S")

    @pd.field_serializer("updated_at")
    def serialize_updated_at(self, v: datetime, _info) -> str:
        return v.strftime("%Y-%m-%d %H:%M:%S")


class TokenData(BaseSchema):
    email: str


class Token(BaseSchema):
    access_token: str
    token_type: str
