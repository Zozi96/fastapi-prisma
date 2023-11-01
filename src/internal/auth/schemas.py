from datetime import datetime
import pydantic as pd


class UserBase(pd.BaseModel):
    email: pd.EmailStr = pd.Field(examples=["john.doe@mail.com"])
    first_name: str | None = pd.Field(default="", max_length=100, examples=["John"])
    last_name: str | None = pd.Field(default="", max_length=100, examples=["Doe"])


class UserForm(UserBase):
    password: str = pd.Field(min_length=8, max_length=32, examples=["mysecretpassword"])


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


class TokenData(pd.BaseModel):
    email: str


class Token(pd.BaseModel):
    access_token: str
    token_type: str
