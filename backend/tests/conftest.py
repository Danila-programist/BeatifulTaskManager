import uuid

import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from main import app
from app.models import Base, User
from app.db import get_db
from app.utils import pwd_manager


TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5433/taskmanager_test"


@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def setup_database(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session(engine: AsyncEngine, setup_database):
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def plain_password():
    return "MySecurePassword123!"


@pytest_asyncio.fixture(scope="function")
async def override_db_session(db_session: AsyncSession):
    async def _get_test_session():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_session
    yield
    app.dependency_overrides.pop(get_db, None)

@pytest_asyncio.fixture(scope="function")
async def authenticated_client(client: AsyncClient, override_db_session, db_session: AsyncSession):
    
    test_user = User(
        user_id=uuid.uuid4(),
        username="testuser",
        email="testuser@example.com",
        password_hash=pwd_manager.hash_password("testpassword123"),
        first_name="Test",
        last_name="User",
        is_active=True
    )
    
    db_session.add