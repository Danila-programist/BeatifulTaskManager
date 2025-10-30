import pytest

from app.models import Task, User


@pytest.mark.asyncio
async def test_task_creation(db_session):

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

    task = Task(title="Test Task", description="Task description", user_id=user.user_id)
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    assert task.task_id is not None
    assert task.user_id == user.user_id
    assert task.user.username == "testuser"
    assert task.title == "Test Task"
    assert task.status == "pending"
