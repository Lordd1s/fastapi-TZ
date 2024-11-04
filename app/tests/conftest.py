import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import Base
from app.main import app
from app.database.session import DataBaseManager

db_test_url = 'sqlite+aiosqlite:///:memory:'


@pytest.fixture(scope="session")
async def test_db_manager():
    db_manager = DataBaseManager(url=db_test_url, db_echo=False)
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield db_manager
    await db_manager.engine.dispose()

@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope='session')
async def db_engine(test_db_manager):
    yield test_db_manager.engine

@pytest.fixture
async def async_db_session(test_db_manager) -> AsyncSession:
    async with test_db_manager.async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def async_client(async_db_session, test_db_manager):
    async def get_test_session():
        async with async_db_session as session:
            yield session

    app.dependency_overrides[test_db_manager.session_dependency] = get_test_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()