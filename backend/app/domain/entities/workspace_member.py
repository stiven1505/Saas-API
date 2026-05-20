"""Workspace member domain entity with role enum."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class Role(str, Enum):
    """Roles a user can hold within a workspace."""

    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    READER = "READER"


@dataclass
class WorkspaceMemberEntity:
    """Pure domain representation of a workspace membership."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    workspace_id: UUID = field(default_factory=uuid4)
    role: Role = Role.READER
    is_active: bool = True
    joined_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
