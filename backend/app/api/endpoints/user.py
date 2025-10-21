from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import LoginUser, RegisterUser, DatabaseUser
from app.services import UserService
from app.db import get_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", summary="Регистрация нового пользователя")
async def register(user: RegisterUser, db: AsyncSession = Depends(get_db)): 
    user_service = UserService(db)
    user_db: Optional[DatabaseUser] = await user_service.get_user(user)

    if user_db is None:
        await user_service.add_new_user(user)
        return {"Message": "User was added to the database"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Incorrect password or nickname",
    )



@auth_router.post("/login", summary="Авторизация пользователя")
async def login(user: LoginUser): ...


@auth_router.post("/logout", summary="Выход пользователя из аккаунта")
async def logout(): ...
