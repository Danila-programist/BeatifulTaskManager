from fastapi import APIRouter



oauth_router = APIRouter(prefix='/auth')


@oauth_router.post('/register', summary="Регистрация нового пользователя")
async def register():
    ...


@oauth_router.post('/login', summary='Авторизация пользователя')
async def login():
    ...


@oauth_router.post('/logout', summary="Выход пользователя из аккаунта")
async def logout():
    ...