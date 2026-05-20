"""SQLAlchemy database models."""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import enum as python_enum


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


class UserModel(Base):
    """SQLAlchemy model for users."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, email={self.email})>"


class WorkspaceModel(Base):
    """SQLAlchemy model for workspaces."""

    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default="")
    owner_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<WorkspaceModel(id={self.id}, name={self.name})>"


class RoleEnum(str, python_enum.Enum):
    """Enum for workspace member roles."""

    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    READER = "READER"


class WorkspaceMemberModel(Base):
    """SQLAlchemy model for workspace members."""

    __tablename__ = "workspace_members"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    workspace_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.READER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<WorkspaceMemberModel(id={self.id}, role={self.role})>"


class ProjectStatus(str, python_enum.Enum):
    """Enum for project status."""

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"
    CANCELLED = "CANCELLED"


class ProjectModel(Base):
    """SQLAlchemy model for projects."""

    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    workspace_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default="")
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE)
    created_by: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<ProjectModel(id={self.id}, name={self.name})>"
