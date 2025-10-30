from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.db import get_db
from app.services import TaskService
from app.api.schemas import DatabaseUser, TaskResponse, TaskRequest

task_router = APIRouter(tags=["tasks"])


@task_router.get("/tasks", summary="Все доступные задачи текущего пользователя")
async def get_all_tasks(
    current_user: DatabaseUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[TaskResponse]:
    task_service = TaskService(db, current_user.username)
    tasks = await task_service.get_user_tasks()
    return [TaskResponse.model_validate(task) for task in tasks]


@task_router.post("/tasks", summary="Создание текущем пользователем новой задачи")
async def create_new_task(
    task_req: TaskRequest,
    current_user: DatabaseUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task_service = TaskService(db, current_user.username)
    task = await task_service.create_task(task_req)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Task was not created"
        )

    return {"message": "Task was added"}


@task_router.get(
    "/tasks/{task_id}",
    summary="Получение информации текущем пользователем о конктреной задаче",
)
async def get_task_by_id(
    task_id: int,
    current_user: DatabaseUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task_service = TaskService(db, current_user.username)
    task = await task_service.get_user_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found or you do not have the acception for this task",
        )

    return task


@task_router.put(
    "/tasks/{task_id}",
    summary="Изменение информации текущем пользователем о своей конректной задаче",
)
async def change_task_by_id(
    task_id: int,
    task_req: TaskRequest,
    current_user: DatabaseUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task_service = TaskService(db, current_user.username)
    updated_task = await task_service.update_task(task_id, task_req)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found or you do not have the acception for this task",
        )

    return updated_task


@task_router.delete(
    "/tasks/{task_id}", summary="Удаление текущем пользователем своей задачи"
)
async def delete_tast_by_id(
    task_id: int,
    current_user: DatabaseUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task_service = TaskService(db, current_user.username)
    is_deleted_task: bool = await task_service.delete_task(task_id)

    if not is_deleted_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found or you do not have the acception for this task",
        )

    return {"message": "task was deleted"}
