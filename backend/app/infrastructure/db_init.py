"""Database configuration and setup."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core import settings
from app.infrastructure.database import Base


async def get_database_engine():
    """Create and return async database engine."""
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
        pool_pre_ping=True,
    )


async def get_session_factory():
    """Create and return async session factory."""
    engine = await get_database_engine()
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


async def init_db():
    """Initialize database tables."""
    engine = await get_database_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def get_db_session():
    """Get database session for dependency injection."""
    engine = await get_database_engine()
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
