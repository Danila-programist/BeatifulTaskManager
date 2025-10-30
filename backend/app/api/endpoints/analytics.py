from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import (
    UserInfo,
    TasksOverview,
    ProductivityMetrics,
    RecentActivity,
    TasksCreatedByWeekday,
    AnalyticsManager,
    DatabaseUser,
)
from app.db import get_db
from app.auth import get_current_user

analytics_router = APIRouter(tags=["analytics"])


@analytics_router.get(
    path="/analytics",
    summary="Основная информация о пользователе и его задачах со статистикой",
)
async def analytics_endpoint(
    current_user: DatabaseUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AnalyticsManager: ...
