import uuid
from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import AnalyticsService
from app.models import User, Task
from app.api.schemas import DatabaseUser
from app.utils import pwd_manager


class TestAnalyticsService:

    @pytest_asyncio.fixture
    async def test_user(self, db_session: AsyncSession):
        user = User(
            user_id=uuid.uuid4(),
            username="testuser",
            email="testuser@example.com",
            password_hash=pwd_manager.hash_password("password123"),
            first_name="Test",
            last_name="User",
            is_active=True,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    @pytest_asyncio.fixture
    async def database_user(self, test_user: User) -> DatabaseUser:
        return DatabaseUser(
            user_id=test_user.user_id,
            username=test_user.username,
            email=test_user.email,
            password_hash=test_user.password_hash,
            first_name=test_user.first_name,
            last_name=test_user.last_name,
            is_active=test_user.is_active,
            created_at=test_user.created_at,
        )

    @pytest_asyncio.fixture
    async def analytics_service(
        self, db_session: AsyncSession, database_user: DatabaseUser
    ):
        return AnalyticsService(db_session, database_user)

    @pytest_asyncio.fixture
    async def test_tasks(self, db_session: AsyncSession, test_user: User):
        tasks = [
            Task(
                title="Completed Task",
                description="A completed task",
                status="completed",
                user_id=test_user.user_id,
                created_at=datetime.now() - timedelta(days=2),
                updated_at=datetime.now() - timedelta(days=1),
            ),
            Task(
                title="In Progress Task",
                description="A task in progress",
                status="in_progress",
                user_id=test_user.user_id,
                created_at=datetime.now() - timedelta(days=1),
            ),
            Task(
                title="Pending Task",
                description="A pending task",
                status="pending",
                user_id=test_user.user_id,
                created_at=datetime.now(),
            ),
            Task(
                title="Inactive Task",
                description="An inactive task",
                status="pending",
                is_active=False,
                user_id=test_user.user_id,
                created_at=datetime.now(),
            ),
        ]

        for task in tasks:
            db_session.add(task)
        await db_session.commit()

        return tasks

    @pytest.mark.asyncio
    async def test_get_user_info_success(
        self, analytics_service: AnalyticsService, test_user: User
    ):
        user_info = await analytics_service.get_user_info()

        assert user_info.username == test_user.username
        assert user_info.email == test_user.email
        assert user_info.first_name == test_user.first_name
        assert user_info.last_name == test_user.last_name

    @pytest.mark.asyncio
    async def test_get_user_info_user_not_found(self, db_session: AsyncSession):
        database_user = DatabaseUser(
            user_id=uuid.uuid4(),
            username="nonexistent",
            email="nonexistent@example.com",
            password_hash="hash",
            first_name="None",
            last_name="Existent",
            is_active=True,
            created_at=datetime.now(),
        )

        service = AnalyticsService(db_session, database_user)

        with pytest.raises(ValueError, match="User nonexistent not found"):
            await service.get_user_info()

    @pytest.mark.asyncio
    async def test_get_tasks_overview_empty(self, analytics_service: AnalyticsService):
        overview = await analytics_service.get_tasks_overview()

        assert overview.total_tasks == 0
        assert overview.active_tasks == 0
        assert overview.completed_tasks == 0
        assert overview.completion_rate is None

    @pytest.mark.asyncio
    async def test_get_tasks_overview_with_tasks(
        self, analytics_service: AnalyticsService, test_tasks
    ):
        overview = await analytics_service.get_tasks_overview()

        assert overview.total_tasks == 3
        assert overview.active_tasks == 1
        assert overview.completed_tasks == 1
        assert overview.completion_rate == pytest.approx(33.33, abs=0.01)

    @pytest.mark.asyncio
    async def test_get_productive_metrics_empty(
        self, analytics_service: AnalyticsService
    ):
        metrics = await analytics_service.get_productive_metrics()

        assert metrics.tasks_created_today == 0
        assert metrics.tasks_completed_today == 0
        assert metrics.tasks_created_this_week == 0
        assert metrics.tasks_completed_this_week == 0

    @pytest.mark.asyncio
    async def test_get_recent_activity_with_tasks(
        self, analytics_service: AnalyticsService, test_tasks
    ):
        activity = await analytics_service.get_recent_activity()

        assert activity.last_task_created is not None

        assert activity.last_task_completed is not None

        assert activity.most_active_day is not None

    @pytest.mark.asyncio
    async def test_get_tasks_created_by_weekday_empty(
        self, analytics_service: AnalyticsService
    ):
        weekday_data = await analytics_service.get_tasks_created_by_weekday()

        assert weekday_data.monday == 0
        assert weekday_data.tuesday == 0
        assert weekday_data.wednesday == 0
        assert weekday_data.thursday == 0
        assert weekday_data.friday == 0
        assert weekday_data.saturday == 0
        assert weekday_data.sunday == 0

    @pytest.mark.asyncio
    async def test_get_tasks_created_by_weekday_with_tasks(
        self,
        analytics_service: AnalyticsService,
        db_session: AsyncSession,
        test_user: User,
    ):
        now = datetime.now()

        monday_task = Task(
            title="Monday Task",
            user_id=test_user.user_id,
            created_at=now - timedelta(days=now.weekday()),
        )

        tuesday_task = Task(
            title="Tuesday Task",
            user_id=test_user.user_id,
            created_at=now - timedelta(days=now.weekday() - 1),
        )

        tuesday_task2 = Task(
            title="Tuesday Task 2",
            user_id=test_user.user_id,
            created_at=now - timedelta(days=now.weekday() - 1),
        )

        for task in [monday_task, tuesday_task, tuesday_task2]:
            db_session.add(task)
        await db_session.commit()

        weekday_data = await analytics_service.get_tasks_created_by_weekday()

        assert weekday_data.monday == 1
        assert weekday_data.tuesday == 2
        assert weekday_data.wednesday == 0
        assert weekday_data.thursday == 0
        assert weekday_data.friday == 0
        assert weekday_data.saturday == 0
        assert weekday_data.sunday == 0

    @pytest.mark.asyncio
    async def test_user_isolation_in_analytics(
        self, db_session: AsyncSession, test_user: User
    ):
        user2 = User(
            user_id=uuid.uuid4(),
            username="user2",
            email="user2@example.com",
            password_hash=pwd_manager.hash_password("password123"),
            first_name="User",
            last_name="Two",
            is_active=True,
        )
        db_session.add(user2)
        await db_session.commit()

        task_user1 = Task(
            title="User1 Task",
            user_id=test_user.user_id,
            status="completed",
        )
        db_session.add(task_user1)
        await db_session.commit()

        database_user2 = DatabaseUser(
            user_id=user2.user_id,
            username=user2.username,
            email=user2.email,
            password_hash=user2.password_hash,
            first_name=user2.first_name,
            last_name=user2.last_name,
            is_active=user2.is_active,
            created_at=user2.created_at,
        )
        service_user2 = AnalyticsService(db_session, database_user2)

        overview = await service_user2.get_tasks_overview()
        assert overview.total_tasks == 0
        assert overview.completed_tasks == 0

    @pytest.mark.asyncio
    async def test_completion_rate_calculation(
        self,
        analytics_service: AnalyticsService,
        db_session: AsyncSession,
        test_user: User,
    ):
        for i in range(5):
            task = Task(
                title=f"Task {i}",
                user_id=test_user.user_id,
                status="completed" if i < 4 else "pending",
            )
            db_session.add(task)
        await db_session.commit()

        overview = await analytics_service.get_tasks_overview()

        assert overview.total_tasks == 5
        assert overview.completed_tasks == 4
        assert overview.completion_rate == 80.0

    @pytest.mark.asyncio
    async def test_completion_rate_zero_division(
        self, analytics_service: AnalyticsService
    ):
        overview = await analytics_service.get_tasks_overview()
        assert overview.completion_rate is None

    @pytest.mark.asyncio
    async def test_only_active_tasks_counted(
        self,
        analytics_service: AnalyticsService,
        db_session: AsyncSession,
        test_user: User,
    ):

        active_task = Task(
            title="Active Task",
            user_id=test_user.user_id,
            status="completed",
            is_active=True,
        )
        inactive_task = Task(
            title="Inactive Task",
            user_id=test_user.user_id,
            status="completed",
            is_active=False,
        )

        db_session.add(active_task)
        db_session.add(inactive_task)
        await db_session.commit()

        overview = await analytics_service.get_tasks_overview()

        assert overview.total_tasks == 1
        assert overview.completed_tasks == 1
        assert overview.completion_rate == 100.0
