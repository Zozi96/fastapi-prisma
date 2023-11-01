import pydantic as pd


class UserBase(pd.BaseModel):
    email: pd.EmailStr


class UserForm(UserBase):
    password: str = pd.Field(min_length=8, max_length=32)


class UserResponse(UserBase):
    id: int


class TokenData(pd.BaseModel):
    email: str


class Token(pd.BaseModel):
    access_token: str
    token_type: str
