from fastapi import APIRouter

from app.api.schemas import LoginUser, RegisterUser

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", summary="Регистрация нового пользователя")
async def register(user: RegisterUser): ...


@auth_router.post("/login", summary="Авторизация пользователя")
async def login(user: LoginUser): ...


@auth_router.post("/logout", summary="Выход пользователя из аккаунта")
async def logout(): ...
