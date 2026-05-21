"""Database seeding script."""

import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from passlib.context import CryptContext

from app.core import settings
from app.infrastructure.database import (
    UserModel,
    WorkspaceModel,
    WorkspaceMemberModel,
    ProjectModel,
    RoleEnum,
    ProjectStatus,
    Base
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_db():
    engine = create_async_engine(settings.DATABASE_URL)
    
    # Ensure tables are created (useful if not using migrations right away)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check if user already exists
        print("SESSION STARTED")
        result = await session.execute(select(UserModel).where(UserModel.email == "test@example.com"))
        user = result.scalar_one_or_none()

        if not user:
            print("Seeding new test user...")
            hashed_pw = pwd_context.hash("password123")
            user = UserModel(
                id="00000000-0000-0000-0000-000000000001",
                email="test@example.com",
                full_name="Test User",
                hashed_password=hashed_pw
            )
            session.add(user)
            await session.flush()
        else:
            print("Test user already exists.")

        # Seed Workspace Alpha
        result = await session.execute(select(WorkspaceModel).where(WorkspaceModel.id == "00000000-0000-0000-0000-000000000002"))
        w_alpha = result.scalar_one_or_none()
        if not w_alpha:
            print("Seeding Workspace Alpha...")
            w_alpha = WorkspaceModel(
                id="00000000-0000-0000-0000-000000000002",
                name="Workspace Alpha",
                description="Alpha workspace description",
                owner_id=user.id
            )
            session.add(w_alpha)
            
            # User ADMIN in Alpha
            wm_alpha = WorkspaceMemberModel(
                id="00000000-0000-0000-0000-000000000003",
                workspace_id=w_alpha.id,
                user_id=user.id,
                role=RoleEnum.ADMIN
            )
            session.add(wm_alpha)
            
            # Example Project in Alpha
            p_alpha = ProjectModel(
                id="00000000-0000-0000-0000-000000000004",
                workspace_id=w_alpha.id,
                name="Project Phoenix",
                description="A top secret AI initiative.",
                status=ProjectStatus.ACTIVE,
                created_by=user.id
            )
            session.add(p_alpha)

        # Seed Workspace Beta
        result = await session.execute(select(WorkspaceModel).where(WorkspaceModel.id == "00000000-0000-0000-0000-000000000005"))
        w_beta = result.scalar_one_or_none()
        if not w_beta:
            print("Seeding Workspace Beta...")
            w_beta = WorkspaceModel(
                id="00000000-0000-0000-0000-000000000005",
                name="Workspace Beta",
                description="Beta workspace description",
                owner_id=user.id
            )
            session.add(w_beta)
            
            # User READER in Beta
            wm_beta = WorkspaceMemberModel(
                id="00000000-0000-0000-0000-000000000006",
                workspace_id=w_beta.id,
                user_id=user.id,
                role=RoleEnum.READER
            )
            session.add(wm_beta)
            
            # Example Project in Beta
            p_beta = ProjectModel(
                id="00000000-0000-0000-0000-000000000007",
                workspace_id=w_beta.id,
                name="Project Titan",
                description="An outdated internal tool.",
                status=ProjectStatus.ON_HOLD,
                created_by=user.id
            )
            session.add(p_beta)

        # Seed Workspace Mega
        result = await session.execute(select(WorkspaceModel).where(WorkspaceModel.id == "00000000-0000-0000-0000-000000000008"))
        w_mega = result.scalar_one_or_none()
        if not w_mega:
            print("Seeding Workspace Mega...")
            w_mega = WorkspaceModel(
                id="00000000-0000-0000-0000-000000000008",
                name="Workspace Mega",
                description="Mega workspace description",
                owner_id=user.id
            )
            session.add(w_mega)

            # User ADMIN in Mega
            wm_mega = WorkspaceMemberModel(
                id="00000000-0000-0000-0000-000000000009",
                workspace_id=w_mega.id,
                user_id=user.id,
                role=RoleEnum.ADMIN
            )
            session.add(wm_mega)

            # Example Project in Mega
            p_mega = ProjectModel(
                id="00000000-0000-0000-0000-000000000010",
                workspace_id=w_mega.id,
                name="Project MEGA",
                description="A revolutionary AI initiative.",
                status=ProjectStatus.ACTIVE,
                created_by=user.id
            )
            session.add(p_mega)
        print("COMMITTING...")
        await session.commit()
        print("Database seeded successfully!")

    await engine.dispose()

if __name__ == "__main__":
    try:
        print("STARTING DATABASE SEED...")
        asyncio.run(seed_db())
        print("SEED FINISHED SUCCESSFULLY")
    except Exception as e:
        print("SEED FAILED:")
        print(e)
        raise e
