"""Core module - configuration and shared exceptions."""

from app.core.config import settings
from app.core.exceptions import (
    AppBaseError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
    ValidationError,
    DatabaseError,
)

__all__ = [
    "settings",
    "AppBaseError",
    "NotFoundError",
    "UnauthorizedError",
    "ForbiddenError",
    "ConflictError",
    "ValidationError",
    "DatabaseError",
]
