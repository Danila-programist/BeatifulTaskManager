from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.db import get_db
from app.services import TaskService
from app.api.schemas import DatabaseUser, TaskResponse, TaskRequest

task_router = APIRouter(tags=["tasks"])


@task_router.get("/tasks")
async def get_all_tasks(
    current_user: DatabaseUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[TaskResponse]:
    task_service = TaskService(db, current_user.username)
    tasks = await task_service.get_user_tasks()
    return [TaskResponse.model_validate(task) for task in tasks]


@task_router.post("/tasks")
async def create_new_task(
    task_req: TaskRequest,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task_service = TaskService(db, current_user.username)
    task = await task_service.create_task(task_req)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Task was not created"
        )

    return {"message": "Task was added"}


@task_router.get("/tasks/{task_id}")
async def get_task_by_id(
    current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)
): ...


@task_router.put("/tasks/{task_id}")
async def change_task_by_id(
    current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)
): ...


@task_router.delete("/tasks/{task_id}")
async def delete_tast_by_id(
    current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)
): ...
