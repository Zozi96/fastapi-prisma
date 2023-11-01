from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from prisma.models import User as UserRecord
from internal.db import User
from internal.auth.security import (
    generate_password_hash,
    login_for_access_token,
    user_logged,
)

from internal.auth.schemas import UserForm, UserResponse, Token

api = APIRouter(prefix="/auth", tags=["auth"])


@api.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserForm) -> UserRecord:
    if await User.find_first(where={"email": data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    data.password = await generate_password_hash(password=data.password)
    user = await User.create(data=data.model_dump())
    return user


@api.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> dict[str, str]:
    access_token = await login_for_access_token(form_data.username, form_data.password)
    return access_token


@api.get("/me", response_model=UserResponse)
async def read_users_me(current_user: user_logged()):
    return current_user
