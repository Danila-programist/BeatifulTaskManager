import pytest
from httpx import AsyncClient

from app.api.schemas import TaskStatus


@pytest.mark.asyncio
async def test_get_all_tasks_empty(authenticated_client: AsyncClient):
    response = await authenticated_client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_task_success(authenticated_client: AsyncClient):
    task_data = {
        "title": "Test Task",
        "description": "Test description",
        "status": TaskStatus.PENDING,
    }

    response = await authenticated_client.post("/api/v1/tasks", json=task_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Task was added"}


@pytest.mark.asyncio
async def test_create_task_invalid_data(authenticated_client: AsyncClient):
    task_data = {
        "title": "T" * 257,
        "description": "Test description",
        "status": TaskStatus.PENDING,
    }

    response = await authenticated_client.post("/api/v1/tasks", json=task_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_tasks_with_data(authenticated_client: AsyncClient):
    tasks_data = [
        {
            "title": "Task 1",
            "description": "Description 1",
            "status": TaskStatus.PENDING,
        },
        {
            "title": "Task 2",
            "description": "Description 2",
            "status": TaskStatus.IN_PROGRESS,
        },
    ]

    for task_data in tasks_data:
        await authenticated_client.post("/api/v1/tasks", json=task_data)

    response = await authenticated_client.get("/api/v1/tasks")
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 2"
    assert tasks[1]["title"] == "Task 1"
    assert "task_id" in tasks[0]
    assert "created_at" in tasks[0]
    assert "user_id" in tasks[0]


@pytest.mark.asyncio
async def test_get_task_by_id_success(authenticated_client: AsyncClient):
    task_data = {
        "title": "Specific Task",
        "description": "Specific description",
        "status": TaskStatus.PENDING,
    }

    create_response = await authenticated_client.post("/api/v1/tasks", json=task_data)
    assert create_response.status_code == 200

    tasks_response = await authenticated_client.get("/api/v1/tasks")
    tasks = tasks_response.json()
    task_id = tasks[0]["task_id"]

    response = await authenticated_client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200

    task = response.json()
    assert task["title"] == "Specific Task"
    assert task["description"] == "Specific description"
    assert task["status"] == TaskStatus.PENDING
    assert task["task_id"] == task_id


@pytest.mark.asyncio
async def test_get_task_by_id_not_found(authenticated_client: AsyncClient):
    response = await authenticated_client.get("/api/v1/tasks/9999")
    assert response.status_code == 404
    assert "Task was not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_task_success(authenticated_client: AsyncClient):
    task_data = {
        "title": "Original Task",
        "description": "Original description",
        "status": TaskStatus.PENDING,
    }

    await authenticated_client.post("/api/v1/tasks", json=task_data)

    tasks_response = await authenticated_client.get("/api/v1/tasks")
    task_id = tasks_response.json()[0]["task_id"]

    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": TaskStatus.IN_PROGRESS,
    }

    response = await authenticated_client.put(
        f"/api/v1/tasks/{task_id}", json=update_data
    )
    assert response.status_code == 200

    updated_task = response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["description"] == "Updated description"
    assert updated_task["status"] == TaskStatus.IN_PROGRESS
    assert updated_task["task_id"] == task_id


@pytest.mark.asyncio
async def test_update_task_not_found(authenticated_client: AsyncClient):
    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": TaskStatus.COMPLETED,
    }

    response = await authenticated_client.put("/api/v1/tasks/9999", json=update_data)
    assert response.status_code == 404
    assert "Task was not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_task_success(authenticated_client: AsyncClient):
    task_data = {
        "title": "Task to delete",
        "description": "Will be deleted",
        "status": TaskStatus.PENDING,
    }

    await authenticated_client.post("/api/v1/tasks", json=task_data)

    tasks_response = await authenticated_client.get("/api/v1/tasks")
    task_id = tasks_response.json()[0]["task_id"]

    response = await authenticated_client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "task was deleted"}

    get_response = await authenticated_client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_not_found(authenticated_client: AsyncClient):
    response = await authenticated_client.delete("/api/v1/tasks/9999")
    assert response.status_code == 404
    assert "Task was not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_task_isolation_between_users(client: AsyncClient, override_db_session):
    user1_data = {
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123",
        "first_name": "User",
        "last_name": "One",
    }
    await client.post("/api/v1/auth/register", json=user1_data)

    login1_data = {"username": "user1", "password": "password123"}
    login_response = await client.post("/api/v1/auth/login", json=login1_data)
    assert login_response.status_code == 200

    task_data = {
        "title": "User1 Task",
        "description": "User1 description",
        "status": TaskStatus.PENDING,
    }
    await client.post("/api/v1/tasks", json=task_data)

    user2_data = {
        "username": "user2",
        "email": "user2@example.com",
        "password": "password123",
        "first_name": "User",
        "last_name": "Two",
    }
    await client.post("/api/v1/auth/register", json=user2_data)

    login2_data = {"username": "user2", "password": "password123"}
    await client.post("/api/v1/auth/login", json=login2_data)

    response = await client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_task_minimal_data(authenticated_client: AsyncClient):
    task_data = {
        "title": "Minimal Task"
        # description и status не обязательны (status имеет значение по умолчанию)
    }

    response = await authenticated_client.post("/api/v1/tasks", json=task_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Task was added"}

    tasks_response = await authenticated_client.get("/api/v1/tasks")
    task = tasks_response.json()[0]
    assert task["title"] == "Minimal Task"
    assert task["description"] is None
    assert task["status"] == TaskStatus.PENDING
