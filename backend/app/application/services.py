"""Application use case services."""

import logging
from typing import List
from uuid import UUID
from app.core import UnauthorizedError, NotFoundError, ConflictError
from app.domain.entities.user import UserEntity
from app.domain.entities.workspace import WorkspaceEntity
from app.domain.entities.workspace_member import WorkspaceMemberEntity, Role
from app.domain.entities.project import ProjectEntity
from app.domain.repositories import (
    UserRepository,
    WorkspaceRepository,
    WorkspaceMemberRepository,
    ProjectRepository,
)
from app.interfaces.auth import AuthUtils
from app.interfaces.schemas import WorkspaceListResponse, WorkspaceResponse

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication operations."""

    def __init__(
        self,
        user_repo: UserRepository,
        member_repo: WorkspaceMemberRepository,
    ):
        self.user_repo = user_repo
        self.member_repo = member_repo

    async def login(self, email: str, password: str) -> dict:
        """Login user and return JWT token.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Login response with token and workspace info
        """
        user = await self.user_repo.get_by_email(email)
        if not user or not AuthUtils.verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedError("User account is inactive")

        # Get user's workspace memberships
        memberships = await self.member_repo.list_by_user(user.id)
        
        workspace_id = ""
        role = ""
        if memberships:
            # Use the first membership (could implement workspace selection later)
            membership = memberships[0]
            workspace_id = str(membership.workspace_id)
            role = membership.role.value

        token = AuthUtils.create_access_token(
            user_id=str(user.id),
            workspace_id=workspace_id,
            role=role,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": str(user.id),
            "workspace_id": workspace_id,
        }


class WorkspaceService:
    """Service for workspace operations."""

    def __init__(
        self,
        workspace_repo: WorkspaceRepository,
        member_repo: WorkspaceMemberRepository,
    ):
        self.workspace_repo = workspace_repo
        self.member_repo = member_repo

    async def get_user_workspaces(self, user_id: UUID) -> List[WorkspaceListResponse]:
        """Get all workspaces for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of workspace with roles
        """
        memberships = await self.member_repo.list_by_user(user_id)
        
        workspaces = []
        for membership in memberships:
            workspace = await self.workspace_repo.get_by_id(membership.workspace_id)
            if workspace:
                workspaces.append(
                    WorkspaceListResponse(
                        id=str(workspace.id),
                        name=workspace.name,
                        description=workspace.description,
                        owner_id=str(workspace.owner_id),
                        is_active=workspace.is_active,
                        created_at=workspace.created_at,
                        role=membership.role.value,
                    )
                )
        
        return workspaces

    async def create_workspace(self, name: str, description: str, owner_id: UUID) -> WorkspaceEntity:
        """Create a new workspace.
        
        Args:
            name: Workspace name
            description: Workspace description
            owner_id: Owner user ID
            
        Returns:
            Created workspace
        """
        workspace = WorkspaceEntity(
            name=name,
            description=description,
            owner_id=owner_id,
        )
        
        created = await self.workspace_repo.create(workspace)
        
        # Add owner as ADMIN member
        member = WorkspaceMemberEntity(
            user_id=owner_id,
            workspace_id=created.id,
            role=Role.ADMIN,
        )
        await self.member_repo.create(member)
        await self.workspace_repo.session.commit()
        
        return created


class ProjectService:
    """Service for project operations."""

    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    async def get_workspace_projects(self, workspace_id: UUID) -> List[ProjectEntity]:
        """Get all projects in a workspace.
        
        Args:
            workspace_id: Workspace ID
            
        Returns:
            List of projects
        """
        return await self.project_repo.list_by_workspace(workspace_id)

    async def create_project(
        self,
        workspace_id: UUID,
        name: str,
        description: str,
        created_by: UUID,
    ) -> ProjectEntity:
        """Create a new project.
        
        Args:
            workspace_id: Workspace ID
            name: Project name
            description: Project description
            created_by: Creator user ID
            
        Returns:
            Created project
        """
        project = ProjectEntity(
            workspace_id=workspace_id,
            name=name,
            description=description,
            created_by=created_by,
        )
        
        return await self.project_repo.create(project)

