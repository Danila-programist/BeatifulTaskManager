import pytest
from sqlalchemy import select

from app.services import UserService
from app.models import User
from app.api.schemas import RegisterUser
from app.utils import pwd_manager


@pytest.mark.asyncio
async def test_add_new_user_creates_user_in_db(db_session):
    service = UserService(db_session)

    user_data = RegisterUser(
        username="testuser",
        email="test@example.com",
        password="SuperSecret123",
        first_name="Test",
        last_name="User",
    )

    await service.add_new_user(user_data)

    result = await db_session.execute(select(User).where(User.username == "testuser"))
    db_user = result.scalar_one_or_none()

    assert db_user is not None
    assert db_user.username == user_data.username
    assert db_user.email == user_data.email

    assert db_user.password_hash != user_data.password
    assert pwd_manager.verify_password(user_data.password, db_user.password_hash)


@pytest.mark.asyncio
async def test_get_user_returns_existing_user(db_session):
    hashed_pwd = pwd_manager.hash_password("Password123")
    user = User(
        username="existing_user",
        email="existing@example.com",
        password_hash=hashed_pwd,
        first_name="Jane",
        last_name="Doe",
    )

    db_session.add(user)
    await db_session.commit()

    service = UserService(db_session)
    fetched_user = await service.get_user("existing_user")

    assert fetched_user is not None
    assert fetched_user.username == "existing_user"
    assert fetched_user.email == "existing@example.com"


@pytest.mark.asyncio
async def test_get_user_returns_none_if_not_found(db_session):
    service = UserService(db_session)
    result = await service.get_user("non_existing_user")
    assert result is None
