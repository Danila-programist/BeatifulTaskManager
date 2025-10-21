from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import LoginUser, RegisterUser, DatabaseUser
from app.services import UserService
from app.db import get_db
from app.utils import pwd_manager
from app.auth import ClientJWT

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", summary="Регистрация нового пользователя")
async def register(user: RegisterUser, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user_db: Optional[DatabaseUser] = await user_service.get_user(user.username)

    if user_db is None:
        await user_service.add_new_user(user)
        return {"Message": "User was added to the database"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Incorrect password or nickname",
    )


@auth_router.post("/login", summary="Авторизация пользователя")
async def login(user: LoginUser, response: Response, db: AsyncSession = Depends(get_db)): 
    user_service = UserService(db)
    user_db: Optional[DatabaseUser] = await user_service.get_user(user.username)

    if user_db and pwd_manager.verify_password(user.password, user_db.password_hash):
        token = ClientJWT(data={"sub": user.username})
        response.set_cookie(key='task_manager_token', value=token.create_token(), httponly=True)
        return {"Message": "User was authorized"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Incorrect password or nickname",
    )



@auth_router.post("/logout", summary="Выход пользователя из аккаунта")
async def logout(response: Response): 
    response.delete_cookie(key="task_manager_token")
    return {"Message": "Successfully logged out"}