"""Abstract workspace repository interface (port)."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.workspace import WorkspaceEntity


class IWorkspaceRepository(ABC):
    """Port that the domain expects for workspace persistence."""

    @abstractmethod
    async def get_by_id(self, workspace_id: UUID) -> Optional[WorkspaceEntity]:
        """Return a workspace by primary key, or None."""
        ...

    @abstractmethod
    async def get_all(self) -> List[WorkspaceEntity]:
        """Return all workspaces."""
        ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[WorkspaceEntity]:
        """Return all workspaces the given user belongs to."""
        ...

    @abstractmethod
    async def create(self, entity: WorkspaceEntity) -> WorkspaceEntity:
        """Persist a new workspace and return the created entity."""
        ...

    @abstractmethod
    async def update(self, entity: WorkspaceEntity) -> WorkspaceEntity:
        """Update an existing workspace and return the updated entity."""
        ...

    @abstractmethod
    async def delete(self, workspace_id: UUID) -> None:
        """Delete a workspace by primary key."""
        ...
