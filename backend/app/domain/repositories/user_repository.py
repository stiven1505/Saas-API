"""Abstract user repository interface (port)."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.entities.user import UserEntity


class IUserRepository(ABC):
    """Port that the domain expects for user persistence."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        """Return a user by primary key, or None."""
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Return a user by email address, or None."""
        ...

    @abstractmethod
    async def create(self, entity: UserEntity) -> UserEntity:
        """Persist a new user and return the created entity."""
        ...

    @abstractmethod
    async def update(self, entity: UserEntity) -> UserEntity:
        """Update an existing user and return the updated entity."""
        ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        """Delete a user by primary key."""
        ...
