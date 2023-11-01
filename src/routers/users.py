from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from prisma.models import User as UserRecord
from internal.db import User
from internal.security import (
    generate_password_hash,
    get_current_user,
    login_for_access_token,
    Token,
)

from schemas.user import UserForm, UserResponse

router = APIRouter(prefix="/users")


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(data: UserForm) -> UserRecord:
    data = data.model_dump()
    if await User.find_first(where={"email": data["email"]}):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email already registered",
        )
    data["password"] = await generate_password_hash(password=data["password"])
    user = await User.create(data=data)
    return user


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[UserForm, Depends()]) -> dict[str, str]:
    access_token = await login_for_access_token(form_data.email, form_data.password)
    return access_token


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    return current_user
