from fastapi import APIRouter


analytics_router = APIRouter(tags=['analytics'])


@analytics_router.get(path="/analytics")
async def analytics_endpoint(): ...
