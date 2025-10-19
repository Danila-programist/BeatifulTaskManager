import pytest

from app.models import User

@pytest.mark.asyncio
async def test_user_creation(db_session):

    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed",
        first_name="Test",
        last_name="User",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)


    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password_hash == "hashed"
    assert user.first_name == "Test"
    assert user.last_name == "User"
