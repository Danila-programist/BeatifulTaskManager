from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.db import get_db

task_router = APIRouter(tags=["tasks"])


@task_router.get("/tasks")
async def get_all_tasks(current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)): 


@task_router.post("/tasks")
async def create_new_task(current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)): ...


@task_router.get("/tasks/{task_id}")
async def get_task_by_id(current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)): ...


@task_router.put("/tasks/{task_id}")
async def change_task_by_id(current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)): ...


@task_router.delete("/tasks/{task_id}")
async def delete_tast_by_id(current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)): ...
