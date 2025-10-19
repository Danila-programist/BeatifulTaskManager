from fastapi import APIRouter



analytics_router = APIRouter()


@analytics_router.get(path="analytics")
async def analytics_endpoint():
    ...