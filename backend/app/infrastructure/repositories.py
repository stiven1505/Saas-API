"""SQLAlchemy repository implementations."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import UserEntity
from app.domain.entities.workspace import WorkspaceEntity
from app.domain.entities.workspace_member import WorkspaceMemberEntity, Role
from app.domain.entities.project import ProjectEntity
from app.domain.repositories import (
    UserRepository,
    WorkspaceRepository,
    WorkspaceMemberRepository,
    ProjectRepository,
)
from app.infrastructure.database import (
    UserModel,
    WorkspaceModel,
    WorkspaceMemberModel,
    ProjectModel,
)


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        """Get user by ID."""
        stmt = select(UserModel).where(UserModel.id == str(user_id))
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return self._to_entity(user) if user else None

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get user by email."""
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return self._to_entity(user) if user else None

    async def create(self, user: UserEntity) -> UserEntity:
        """Create a new user."""
        model = UserModel(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_entity(model)

    async def update(self, user: UserEntity) -> UserEntity:
        """Update an existing user."""
        stmt = select(UserModel).where(UserModel.id == str(user.id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.email = user.email
            model.full_name = user.full_name
            model.hashed_password = user.hashed_password
            model.is_active = user.is_active
            await self.session.flush()
        return user

    @staticmethod
    def _to_entity(model: UserModel) -> UserEntity:
        """Convert model to entity."""
        return UserEntity(
            id=UUID(model.id),
            email=model.email,
            full_name=model.full_name,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyWorkspaceRepository(WorkspaceRepository):
    """SQLAlchemy implementation of WorkspaceRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, workspace_id: UUID) -> Optional[WorkspaceEntity]:
        """Get workspace by ID."""
        stmt = select(WorkspaceModel).where(WorkspaceModel.id == str(workspace_id))
        result = await self.session.execute(stmt)
        workspace = result.scalar_one_or_none()
        return self._to_entity(workspace) if workspace else None

    async def list_by_owner(self, owner_id: UUID) -> List[WorkspaceEntity]:
        """List workspaces by owner."""
        stmt = select(WorkspaceModel).where(WorkspaceModel.owner_id == str(owner_id))
        result = await self.session.execute(stmt)
        workspaces = result.scalars().all()
        return [self._to_entity(w) for w in workspaces]

    async def create(self, workspace: WorkspaceEntity) -> WorkspaceEntity:
        """Create a new workspace."""
        model = WorkspaceModel(
            id=str(workspace.id),
            name=workspace.name,
            description=workspace.description,
            owner_id=str(workspace.owner_id),
            is_active=workspace.is_active,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_entity(model)

    async def update(self, workspace: WorkspaceEntity) -> WorkspaceEntity:
        """Update an existing workspace."""
        stmt = select(WorkspaceModel).where(WorkspaceModel.id == str(workspace.id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.name = workspace.name
            model.description = workspace.description
            model.is_active = workspace.is_active
            await self.session.flush()
        return workspace

    @staticmethod
    def _to_entity(model: WorkspaceModel) -> WorkspaceEntity:
        """Convert model to entity."""
        return WorkspaceEntity(
            id=UUID(model.id),
            name=model.name,
            description=model.description,
            owner_id=UUID(model.owner_id),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyWorkspaceMemberRepository(WorkspaceMemberRepository):
    """SQLAlchemy implementation of WorkspaceMemberRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, member_id: UUID) -> Optional[WorkspaceMemberEntity]:
        """Get workspace member by ID."""
        stmt = select(WorkspaceMemberModel).where(WorkspaceMemberModel.id == str(member_id))
        result = await self.session.execute(stmt)
        member = result.scalar_one_or_none()
        return self._to_entity(member) if member else None

    async def get_by_user_and_workspace(
        self, user_id: UUID, workspace_id: UUID
    ) -> Optional[WorkspaceMemberEntity]:
        """Get workspace member by user and workspace."""
        stmt = select(WorkspaceMemberModel).where(
            (WorkspaceMemberModel.user_id == str(user_id))
            & (WorkspaceMemberModel.workspace_id == str(workspace_id))
        )
        result = await self.session.execute(stmt)
        member = result.scalar_one_or_none()
        return self._to_entity(member) if member else None

    async def list_by_workspace(self, workspace_id: UUID) -> List[WorkspaceMemberEntity]:
        """List members of a workspace."""
        stmt = select(WorkspaceMemberModel).where(
            WorkspaceMemberModel.workspace_id == str(workspace_id)
        )
        result = await self.session.execute(stmt)
        members = result.scalars().all()
        return [self._to_entity(m) for m in members]

    async def list_by_user(self, user_id: UUID) -> List[WorkspaceMemberEntity]:
        """List workspaces a user belongs to."""
        stmt = select(WorkspaceMemberModel).where(
            WorkspaceMemberModel.user_id == str(user_id)
        )
        result = await self.session.execute(stmt)
        members = result.scalars().all()
        return [self._to_entity(m) for m in members]

    async def create(self, member: WorkspaceMemberEntity) -> WorkspaceMemberEntity:
        """Create a new workspace member."""
        model = WorkspaceMemberModel(
            id=str(member.id),
            workspace_id=str(member.workspace_id),
            user_id=str(member.user_id),
            role=member.role,
            is_active=member.is_active,
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_entity(model)

    async def update(self, member: WorkspaceMemberEntity) -> WorkspaceMemberEntity:
        """Update an existing workspace member."""
        stmt = select(WorkspaceMemberModel).where(WorkspaceMemberModel.id == str(member.id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.role = member.role
            model.is_active = member.is_active
            await self.session.flush()
        return member

    @staticmethod
    def _to_entity(model: WorkspaceMemberModel) -> WorkspaceMemberEntity:
        """Convert model to entity."""
        return WorkspaceMemberEntity(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            workspace_id=UUID(model.workspace_id),
            role=Role[model.role.value],
            is_active=model.is_active,
            joined_at=model.joined_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyProjectRepository(ProjectRepository):
    """SQLAlchemy implementation of ProjectRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, project_id: UUID) -> Optional[ProjectEntity]:
        """Get project by ID."""
        stmt = select(ProjectModel).where(ProjectModel.id == str(project_id))
        result = await self.session.execute(stmt)
        project = result.scalar_one_or_none()
        return self._to_entity(project) if project else None

    async def list_by_workspace(self, workspace_id: UUID) -> List[ProjectEntity]:
        """List projects in a workspace."""
        stmt = select(ProjectModel).where(ProjectModel.workspace_id == str(workspace_id))
        result = await self.session.execute(stmt)
        projects = result.scalars().all()
        return [self._to_entity(p) for p in projects]

    async def create(self, project: ProjectEntity) -> ProjectEntity:
        """Create a new project."""
        model = ProjectModel(
            id=str(project.id),
            workspace_id=str(project.workspace_id),
            name=project.name,
            description=project.description,
            status=project.status,
            created_by=str(project.created_by),
            is_active=project.is_active,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def update(self, project: ProjectEntity) -> ProjectEntity:
        """Update an existing project."""
        stmt = select(ProjectModel).where(ProjectModel.id == str(project.id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.name = project.name
            model.description = project.description
            model.status = project.status
            model.is_active = project.is_active
            await self.session.flush()
        return project

    @staticmethod
    def _to_entity(model: ProjectModel) -> ProjectEntity:
        """Convert model to entity."""
        from app.domain.entities.project import ProjectStatus

        return ProjectEntity(
            id=UUID(model.id),
            workspace_id=UUID(model.workspace_id),
            name=model.name,
            description=model.description,
            status=ProjectStatus[model.status.value],
            created_by=UUID(model.created_by),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
