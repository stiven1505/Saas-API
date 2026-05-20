"""Test configuration and fixtures."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core import settings
from app.main import app
from app.infrastructure.database import Base


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def test_db():
    """Create test database."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    yield async_session
    
    await engine.dispose()


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_user_data():
    """Test user data."""
    return {
        "email": "test@example.com",
        "password": "Test123!@",
        "full_name": "Test User"
    }


@pytest.fixture
def test_workspace_data():
    """Test workspace data."""
    return {
        "name": "Test Workspace",
        "description": "A workspace for testing"
    }


@pytest.fixture
def test_project_data():
    """Test project data."""
    return {
        "name": "Test Project",
        "description": "A project for testing",
        "status": "ACTIVE"
    }
