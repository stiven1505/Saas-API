"""Repository interfaces for the domain layer."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.user import UserEntity
from app.domain.entities.workspace import WorkspaceEntity
from app.domain.entities.workspace_member import WorkspaceMemberEntity
from app.domain.entities.project import ProjectEntity


class UserRepository(ABC):
    """Abstract repository for User entities."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        """Get user by ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get user by email."""
        pass

    @abstractmethod
    async def create(self, user: UserEntity) -> UserEntity:
        """Create a new user."""
        pass

    @abstractmethod
    async def update(self, user: UserEntity) -> UserEntity:
        """Update an existing user."""
        pass


class WorkspaceRepository(ABC):
    """Abstract repository for Workspace entities."""

    @abstractmethod
    async def get_by_id(self, workspace_id: UUID) -> Optional[WorkspaceEntity]:
        """Get workspace by ID."""
        pass

    @abstractmethod
    async def list_by_owner(self, owner_id: UUID) -> List[WorkspaceEntity]:
        """List workspaces by owner."""
        pass

    @abstractmethod
    async def create(self, workspace: WorkspaceEntity) -> WorkspaceEntity:
        """Create a new workspace."""
        pass

    @abstractmethod
    async def update(self, workspace: WorkspaceEntity) -> WorkspaceEntity:
        """Update an existing workspace."""
        pass


class WorkspaceMemberRepository(ABC):
    """Abstract repository for WorkspaceMember entities."""

    @abstractmethod
    async def get_by_id(self, member_id: UUID) -> Optional[WorkspaceMemberEntity]:
        """Get workspace member by ID."""
        pass

    @abstractmethod
    async def get_by_user_and_workspace(
        self, user_id: UUID, workspace_id: UUID
    ) -> Optional[WorkspaceMemberEntity]:
        """Get workspace member by user and workspace."""
        pass

    @abstractmethod
    async def list_by_workspace(self, workspace_id: UUID) -> List[WorkspaceMemberEntity]:
        """List members of a workspace."""
        pass

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> List[WorkspaceMemberEntity]:
        """List workspaces a user belongs to."""
        pass

    @abstractmethod
    async def create(self, member: WorkspaceMemberEntity) -> WorkspaceMemberEntity:
        """Create a new workspace member."""
        pass

    @abstractmethod
    async def update(self, member: WorkspaceMemberEntity) -> WorkspaceMemberEntity:
        """Update an existing workspace member."""
        pass


class ProjectRepository(ABC):
    """Abstract repository for Project entities."""

    @abstractmethod
    async def get_by_id(self, project_id: UUID) -> Optional[ProjectEntity]:
        """Get project by ID."""
        pass

    @abstractmethod
    async def list_by_workspace(self, workspace_id: UUID) -> List[ProjectEntity]:
        """List projects in a workspace."""
        pass

    @abstractmethod
    async def create(self, project: ProjectEntity) -> ProjectEntity:
        """Create a new project."""
        pass

    @abstractmethod
    async def update(self, project: ProjectEntity) -> ProjectEntity:
        """Update an existing project."""
        pass
