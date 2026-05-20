"""API routes for projects."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.interfaces.schemas import ProjectCreate, ProjectResponse
from app.interfaces.routes_auth import get_current_user
from app.interfaces.auth import TokenData
from app.application.services import ProjectService
from app.domain.repositories import ProjectRepository, WorkspaceMemberRepository
from app.infrastructure.repositories import (
    SQLAlchemyProjectRepository,
    SQLAlchemyWorkspaceMemberRepository,
)
from app.infrastructure.db_init import get_db_session
from app.core import NotFoundError, UnauthorizedError
from fastapi import Header


router = APIRouter(prefix="/api/projects", tags=["projects"])


async def get_project_repository(session: AsyncSession = Depends(get_db_session)) -> ProjectRepository:
    """Get project repository dependency."""
    return SQLAlchemyProjectRepository(session)


async def get_workspace_member_repository(session: AsyncSession = Depends(get_db_session)) -> WorkspaceMemberRepository:
    """Get workspace member repository dependency."""
    return SQLAlchemyWorkspaceMemberRepository(session)


async def get_project_service(
    project_repo: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    """Get project service dependency."""
    return ProjectService(project_repo)


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    x_workspace_id: str = Header(...),
    current_user: TokenData = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
):
    """List projects in current workspace."""
    try:
        workspace_id = UUID(x_workspace_id)
        projects = await project_service.get_workspace_projects(workspace_id)
        return [
            ProjectResponse(
                id=str(p.id),
                workspace_id=str(p.workspace_id),
                name=p.name,
                description=p.description,
                status=p.status.value,
                created_by=str(p.created_by),
                is_active=p.is_active,
                created_at=p.created_at,
            )
            for p in projects
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: ProjectCreate,
    x_workspace_id: str = Header(...),
    current_user: TokenData = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    member_repo: WorkspaceMemberRepository = Depends(get_workspace_member_repository),
):
    """Create a new project.
    
    Requires:
    - Authentication
    - ADMIN or EDITOR role in the workspace
    """
    try:
        workspace_id = UUID(x_workspace_id)
        user_id = UUID(current_user.user_id)
        
        # Check if user is member of the workspace and has appropriate role
        membership = await member_repo.get_by_user_and_workspace(user_id, workspace_id)
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this workspace",
            )
        
        # Check if user has ADMIN or EDITOR role
        if membership.role.value not in ["ADMIN", "EDITOR"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only ADMIN or EDITOR can create projects",
            )
        
        project = await project_service.create_project(
            workspace_id=workspace_id,
            name=request.name,
            description=request.description,
            created_by=user_id,
        )
        
        return ProjectResponse(
            id=str(project.id),
            workspace_id=str(project.workspace_id),
            name=project.name,
            description=project.description,
            status=project.status.value,
            created_by=str(project.created_by),
            is_active=project.is_active,
            created_at=project.created_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
