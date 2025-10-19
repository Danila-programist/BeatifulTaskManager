from fastapi import APIRouter


auth_router = APIRouter(prefix="/auth", tags=['oauth'])


@auth_router.post("/register", summary="Регистрация нового пользователя")
async def register(): 
    ...



@auth_router.post("/login", summary="Авторизация пользователя")
async def login(): ...


@auth_router.post("/logout", summary="Выход пользователя из аккаунта")
async def logout(): ...
