import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, override_db_session):
    user_data = {
        "username": "testuser1",
        "email": "testuser1@example.com",
        "password": "StrongPass123",
        "first_name": "Test",
        "last_name": "User",
    }

    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"Message": "User was added to the database"}


@pytest.mark.asyncio
async def test_register_existing_user_fails(client: AsyncClient, override_db_session):
    user_data = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "StrongPass123",
        "first_name": "Test",
        "last_name": "User",
    }
    await client.post("api/v1/auth/register", json=user_data)

    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Incorrect password or nickname"


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, override_db_session):
    user_data = {
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "StrongPass123",
        "first_name": "Login",
        "last_name": "User",
    }
    await client.post("/api/v1/auth/register", json=user_data)

    login_data = {"username": "loginuser", "password": "StrongPass123"}
    response = await client.post("api/v1/auth/login", json=login_data)

    assert response.status_code == 200
    assert response.json() == {"Message": "User was authorized"}
    assert "task_manager_token" in response.cookies


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, override_db_session):
    user_data = {
        "username": "wrongpassuser",
        "email": "wrongpassuser@example.com",
        "password": "StrongPass123",
        "first_name": "Wrong",
        "last_name": "User",
    }
    await client.post("api/v1/auth/register", json=user_data)

    login_data = {"username": "wrongpassuser", "password": "WrongPass"}
    response = await client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Incorrect password or nickname"


@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient, override_db_session):
    response = await client.post("api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"Message": "Successfully logged out"}
