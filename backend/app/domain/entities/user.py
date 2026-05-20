"""User domain entity."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class UserEntity:
    """Pure domain representation of a user – no ORM dependency."""

    id: UUID = field(default_factory=uuid4)
    email: str = ""
    full_name: str = ""
    hashed_password: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
