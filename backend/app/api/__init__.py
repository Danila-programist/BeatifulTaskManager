from fastapi import APIRouter

from api.endpoints import analytics_router, task_router, oauth_router


router = APIRouter(prefix='/api/v1')
router.include_router(analytics_router, task_router, oauth_router)


__all__ = ['router']