import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.task import TaskService
from app.models import Task, User
from app.api.schemas import TaskRequest, TaskStatus
from app.utils import pwd_manager


class TestTaskService:


    @pytest_asyncio.fixture
    async def test_user(self, db_session: AsyncSession):
        user = User(
            user_id=uuid4(),
            username="testuser",
            email="testuser@example.com",
            password_hash=pwd_manager.hash_password("password123"),
            first_name="Test",
            last_name="User",
            is_active=True
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    @pytest_asyncio.fixture
    async def task_service(self, db_session: AsyncSession, test_user: User):
        return TaskService(db_session, test_user.username)

    @pytest.mark.asyncio
    async def test_get_user_id_success(self, task_service: TaskService, test_user: User):
       
        user_id = await task_service._get_user_id()
        assert user_id == test_user.user_id

    @pytest.mark.asyncio
    async def test_get_user_id_not_found(self, db_session: AsyncSession):
       
        service = TaskService(db_session, "nonexistent_user")
        user_id = await service._get_user_id()
        assert user_id is None

    @pytest.mark.asyncio
    async def test_get_user_tasks_empty(self, task_service: TaskService):
    
        tasks = await task_service.get_user_tasks()
        assert tasks == []

    @pytest.mark.asyncio
    async def test_create_task_success(self, task_service: TaskService):
        
        task_data = TaskRequest(
            title="Test Task",
            description="Test Description",
            status=TaskStatus.PENDING
        )
        
        task = await task_service.create_task(task_data)
        assert task is not None
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == TaskStatus.PENDING
        assert task.is_active == True

    @pytest.mark.asyncio
    async def test_create_task_user_not_found(self, db_session: AsyncSession):
       
        service = TaskService(db_session, "nonexistent_user")
        task_data = TaskRequest(title="Test Task")
        
        task = await service.create_task(task_data)
        assert task is None

    @pytest.mark.asyncio
    async def test_get_user_tasks_with_data(self, task_service: TaskService):

        tasks_data = [
            TaskRequest(title="Task 1", description="Desc 1"),
            TaskRequest(title="Task 2", description="Desc 2", status=TaskStatus.IN_PROGRESS),
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            task = await task_service.create_task(task_data)
            created_tasks.append(task)
       
        tasks = await task_service.get_user_tasks()
        assert len(tasks) == 2
        

        assert tasks[0].title == "Task 2"
        assert tasks[1].title == "Task 1"

    @pytest.mark.asyncio
    async def test_get_user_task_by_id_success(self, task_service: TaskService):
        task_data = TaskRequest(title="Specific Task", description="Specific Desc")
        created_task = await task_service.create_task(task_data)
        
        task = await task_service.get_user_task_by_id(created_task.task_id)
        assert task is not None
        assert task.task_id == created_task.task_id
        assert task.title == "Specific Task"

    @pytest.mark.asyncio
    async def test_get_user_task_by_id_not_found(self, task_service: TaskService):
        task = await task_service.get_user_task_by_id(9999)
        assert task is None

    @pytest.mark.asyncio
    async def test_get_user_task_by_id_wrong_user(self, db_session: AsyncSession, test_user: User):
        other_user = User(
            user_id=uuid4(),
            username="otheruser",
            email="other@example.com",
            password_hash=pwd_manager.hash_password("password123"),
            first_name="Other",
            last_name="User",
            is_active=True
        )
        db_session.add(other_user)
        await db_session.commit()
        
        service1 = TaskService(db_session, test_user.username)
        task_data = TaskRequest(title="Other User Task")
        created_task = await service1.create_task(task_data)
        
        service2 = TaskService(db_session, "otheruser")
        task = await service2.get_user_task_by_id(created_task.task_id)
        assert task is None

    @pytest.mark.asyncio
    async def test_update_task_success(self, task_service: TaskService):
        original_data = TaskRequest(title="Original Task", description="Original Desc")
        created_task = await task_service.create_task(original_data)
        

        update_data = TaskRequest(
            title="Updated Task", 
            description="Updated Desc",
            status=TaskStatus.COMPLETED
        )
        updated_task = await task_service.update_task(created_task.task_id, update_data)
        
        assert updated_task is not None
        assert updated_task.task_id == created_task.task_id
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Desc"
        assert updated_task.status == TaskStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_update_task_partial(self, task_service: TaskService):
        created_task = await task_service.create_task(
            TaskRequest(title="Original", description="Original Desc")
        )
        
        update_data = TaskRequest(title="Updated Title")
        updated_task = await task_service.update_task(created_task.task_id, update_data)
        
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original Desc" 
        assert updated_task.status == TaskStatus.PENDING  

    @pytest.mark.asyncio
    async def test_update_task_not_found(self, task_service: TaskService):
        update_data = TaskRequest(title="Updated Task")
        result = await task_service.update_task(9999, update_data)
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_task_success(self, task_service: TaskService):
        created_task = await task_service.create_task(TaskRequest(title="Task to delete"))
        

        result = await task_service.delete_task(created_task.task_id)
        assert result is True

        task = await task_service.get_user_task_by_id(created_task.task_id)
        assert task is None

        from sqlalchemy import select
        stmt = select(Task).where(Task.task_id == created_task.task_id)
        db_task = (await task_service._session.execute(stmt)).scalar_one()
        assert db_task.is_active == False

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, task_service: TaskService):
        result = await task_service.delete_task(9999)
        assert result is False

    @pytest.mark.asyncio
    async def test_task_isolation_between_users(self, db_session: AsyncSession, test_user: User):
        user2 = User(
            user_id=uuid4(),
            username="user2",
            email="user2@example.com",
            password_hash=pwd_manager.hash_password("password123"),
            first_name="User",
            last_name="Two",
            is_active=True
        )
        db_session.add(user2)
        await db_session.commit()
        
        service1 = TaskService(db_session, test_user.username)
        service2 = TaskService(db_session, "user2")
        

        await service1.create_task(TaskRequest(title="User1 Task"))
        

        tasks_user2 = await service2.get_user_tasks()
        assert tasks_user2 == []

    @pytest.mark.asyncio
    async def test_create_task_minimal_data(self, task_service: TaskService):
        task_data = TaskRequest(title="Minimal Task")
        task = await task_service.create_task(task_data)
        
        assert task is not None
        assert task.title == "Minimal Task"
        assert task.description is None
        assert task.status == TaskStatus.PENDING  