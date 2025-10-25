from fastapi import APIRouter


analytics_router = APIRouter(tags=["analytics"])


@analytics_router.get(
    path="/analytics",
    summary="Основная информация о пользователе и его задачах со статистикой",
)
async def analytics_endpoint(): ...
