from fastapi import APIRouter

from app.api.endpoints import analytics_router, task_router, auth_router


router = APIRouter(prefix="/api/v1")
router.include_router(analytics_router)
router.include_router(task_router)
router.include_router(auth_router)


__all__ = ["router"]
