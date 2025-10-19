from fastapi import APIRouter


task_router = APIRouter()


@task_router.get("/tasks")
async def get_all_tasks(): ...


@task_router.post("/tasks")
async def create_new_task(): ...


@task_router.get("/tasks/{task_id}")
async def get_task_by_id(): ...


@task_router.put("/tasks/{task_id}")
async def change_task_by_id(): ...


@task_router.delete("/tasks/{task_id}")
async def delete_tast_by_id(): ...
