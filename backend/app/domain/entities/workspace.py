"""Workspace domain entity."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class WorkspaceEntity:
    """Pure domain representation of a workspace."""

    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""
    owner_id: UUID = field(default_factory=uuid4)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
