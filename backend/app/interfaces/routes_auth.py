"""API routes for authentication."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import settings, UnauthorizedError
from app.interfaces.schemas import LoginRequest, TokenResponse, UserCreate, UserResponse, TokenRequest
from app.interfaces.auth import AuthUtils, TokenData
from app.application.services import AuthService
from app.domain.repositories import UserRepository
from app.infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyWorkspaceMemberRepository
from app.infrastructure.db_init import get_db_session
from uuid import UUID
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/api/auth", tags=["auth"])

security = HTTPBearer()

async def get_user_repository(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    """Get user repository dependency."""
    return SQLAlchemyUserRepository(session)


async def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    session: AsyncSession = Depends(get_db_session),
) -> AuthService:
    """Get auth service dependency."""
    member_repo = SQLAlchemyWorkspaceMemberRepository(session)
    return AuthService(user_repo, member_repo)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Login endpoint.
    
    Returns:
        JWT token and workspace information
    """
    try:
        result = await auth_service.login(request.email, request.password)
        return result
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=e.detail)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = AuthUtils.decode_token(token)
        user_id = payload.get("sub")
        workspace_id = payload.get("workspace_id", "")
        role = payload.get("role", "")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return TokenData(user_id, workspace_id, role)
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=e.detail)

@router.post("/token", response_model=TokenResponse)
async def exchange_token_with_workspace(
    request: TokenRequest,
    current_user: TokenData = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    """Exchange token for a new one with workspace context.
    
    Validates that the user is a member of the selected workspace and returns
    a new token with the workspace_id and role embedded.
    
    Args:
        request: Token request with workspace_id
        current_user: Current authenticated user from JWT
        session: Database session
        
    Returns:
        New JWT token with updated workspace context
    """
    try:
        from uuid import UUID
        from app.infrastructure.repositories import SQLAlchemyWorkspaceMemberRepository
        
        user_id = UUID(current_user.user_id)
        workspace_id = UUID(request.workspace_id)
        
        # Verify user is a member of the workspace
        member_repo = SQLAlchemyWorkspaceMemberRepository(session)
        membership = await member_repo.get_by_user_and_workspace(user_id, workspace_id)
        
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this workspace",
            )
        
        # Create new token with the selected workspace
        token = AuthUtils.create_access_token(
            user_id=user_id,
            workspace_id=workspace_id,
            role=membership.role.value,
        )
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": str(user_id),
            "workspace_id": str(workspace_id),
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid workspace ID: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


