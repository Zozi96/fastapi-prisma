from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from prisma.models import User as UserRecord

from internal.auth.schemas import UserChangePassword, UserForm, UserResponse, Token
from internal.auth.security import (
    generate_password_hash,
    login_for_access_token,
    user_logged,
    verify_password, add_access_token_blacklist,
)
from internal.db import User

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
async def read_users_me(current_user: user_logged()) -> UserResponse:
    return current_user


@api.patch("/change-password", status_code=status.HTTP_200_OK)
async def change_password(data: UserChangePassword, current_user: user_logged()) -> dict[str, str]:
    if not await verify_password(data.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Old password wrong",
        )
    hashed_password = await generate_password_hash(password=data.new_password)
    await User.update(where={"id": current_user.id}, data={"password": hashed_password})
    return {"message": "Password updated successfully"}


# @api.post("/logout", status_code=status.HTTP_200_OK)
# async def logout(current_user: user_logged()) -> dict[str, str]:
#     await add_access_token_blacklist(token, current_user)
#     return {"message": "Logout successfully"}
