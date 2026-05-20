"""API routes for workspaces."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.interfaces.schemas import WorkspaceCreate, WorkspaceResponse, WorkspaceListResponse, TokenResponse
from app.interfaces.routes_auth import get_current_user
from app.interfaces.auth import TokenData, AuthUtils
from app.application.services import WorkspaceService
from app.domain.repositories import WorkspaceRepository, WorkspaceMemberRepository
from app.infrastructure.repositories import (
    SQLAlchemyWorkspaceRepository,
    SQLAlchemyWorkspaceMemberRepository,
)
from app.infrastructure.db_init import get_db_session


router = APIRouter(prefix="/api/workspaces", tags=["workspaces"])


async def get_workspace_repository(session: AsyncSession = Depends(get_db_session)) -> WorkspaceRepository:
    """Get workspace repository dependency."""
    return SQLAlchemyWorkspaceRepository(session)


async def get_workspace_member_repository(session: AsyncSession = Depends(get_db_session)) -> WorkspaceMemberRepository:
    """Get workspace member repository dependency."""
    return SQLAlchemyWorkspaceMemberRepository(session)


async def get_workspace_service(
    workspace_repo: WorkspaceRepository = Depends(get_workspace_repository),
    member_repo: WorkspaceMemberRepository = Depends(get_workspace_member_repository),
) -> WorkspaceService:
    """Get workspace service dependency."""
    return WorkspaceService(workspace_repo, member_repo)


@router.get("", response_model=List[WorkspaceListResponse])
async def list_user_workspaces(
    current_user: TokenData = Depends(get_current_user),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
):
    """List workspaces for current user."""
    try:
        user_id = UUID(current_user.user_id)
        workspaces = await workspace_service.get_user_workspaces(user_id)
        return workspaces
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    request: WorkspaceCreate,
    current_user: TokenData = Depends(get_current_user),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
):
    """Create a new workspace."""
    try:
        owner_id = UUID(current_user.user_id)
        workspace = await workspace_service.create_workspace(
            name=request.name,
            description=request.description,
            owner_id=owner_id,
        )
        
        return WorkspaceResponse(
            id=str(workspace.id),
            name=workspace.name,
            description=workspace.description,
            owner_id=str(workspace.owner_id),
            is_active=workspace.is_active,
            created_at=workspace.created_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{workspace_id}/select", response_model=TokenResponse)
async def select_workspace(
    workspace_id: UUID,
    current_user: TokenData = Depends(get_current_user),
    member_repo: WorkspaceMemberRepository = Depends(get_workspace_member_repository),
):
    """Select an active workspace and return a new token with updated workspace info.
    
    Args:
        workspace_id: ID of the workspace to select
        current_user: Current authenticated user
        member_repo: Workspace member repository
        
    Returns:
        New JWT token with updated workspace_id and role
    """
    try:
        user_id = UUID(current_user.user_id)
        
        # Check if user is member of the workspace
        membership = await member_repo.get_by_user_and_workspace(user_id, workspace_id)
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this workspace",
            )
        
        # Create new token with the selected workspace
        new_token = AuthUtils.create_access_token(
            user_id=user_id,
            workspace_id=workspace_id,
            role=membership.role.value,
        )
        
        return {
            "access_token": new_token,
            "token_type": "bearer",
            "user_id": str(user_id),
            "workspace_id": str(workspace_id),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
