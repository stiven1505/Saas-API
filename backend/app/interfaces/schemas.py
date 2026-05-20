"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ──── Auth Schemas ──────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"
    user_id: str
    workspace_id: str


# ──── User Schemas ──────────────────────────────────────────────────────

class UserCreate(BaseModel):
    """User creation schema."""

    email: EmailStr
    password: str
    full_name: str


class UserResponse(BaseModel):
    """User response schema."""

    id: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ──── Workspace Schemas ─────────────────────────────────────────────────

class WorkspaceCreate(BaseModel):
    """Workspace creation schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=1000)


class WorkspaceResponse(BaseModel):
    """Workspace response schema."""

    id: str
    name: str
    description: Optional[str] = None
    owner_id: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class WorkspaceListResponse(BaseModel):
    """Workspace list with role and description schema."""

    id: str
    name: str
    description: Optional[str] = None
    role: str
    created_at: datetime


# ──── Project Schemas ────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    """Project creation schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=1000)
    status: str = Field(default="ACTIVE")


class ProjectResponse(BaseModel):
    """Project response schema."""

    id: str
    workspace_id: str
    name: str
    description: str
    status: str
    created_by: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True



# ──── Error Response Schema ──────────────────────────────────────────────

class ErrorResponse(BaseModel):
    """Error response schema."""

    detail: str
    error_code: Optional[str] = None
