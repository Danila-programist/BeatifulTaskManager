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
from app.services import AnalyticsService
from app.utils import logger

analytics_router = APIRouter(tags=["analytics"])


@analytics_router.get(
    path="/analytics",
    summary="Основная информация о пользователе и его задачах со статистикой",
)
async def analytics_endpoint(
    current_user: DatabaseUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AnalyticsManager:
    logger.info("Получен доступ к ручке аналитики")
    analytics_service = AnalyticsService(db, current_user)
    user_info: UserInfo = await analytics_service.get_user_info()
    tasks_overview: TasksOverview = await analytics_service.get_tasks_overview()
    productive_mertics: ProductivityMetrics = (
        await analytics_service.get_productive_metrics()
    )
    recent_activity: RecentActivity = await analytics_service.get_recent_activity()
    tasks_created_by_weekday: TasksCreatedByWeekday = (
        await analytics_service.get_tasks_created_by_weekday()
    )
    logger.info("Вывод ручки аналитики")
    return AnalyticsManager(
        user_info=user_info,
        tasks_overview=tasks_overview,
        productivity_metrics=productive_mertics,
        recent_activity=recent_activity,
        tasks_created_by_weekday=tasks_created_by_weekday,
    )
