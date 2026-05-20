"""Project domain entity with status enum."""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class ProjectStatus(str, Enum):
    """Lifecycle status of a project."""

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"
    CANCELLED = "CANCELLED"


@dataclass
class ProjectEntity:
    """Pure domain representation of a project."""

    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""
    status: ProjectStatus = ProjectStatus.ACTIVE
    workspace_id: UUID = field(default_factory=uuid4)
    created_by: UUID = field(default_factory=uuid4)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
