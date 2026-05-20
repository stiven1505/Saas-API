"""Authentication and JWT utilities."""

import logging
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
import jwt
from passlib.context import CryptContext
from app.core import settings, UnauthorizedError

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUtils:
    """Utilities for authentication."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        user_id: UUID,
        workspace_id: UUID,
        role: str,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Create a JWT access token.
        
        Args:
            user_id: User ID
            workspace_id: Workspace ID
            role: User role in workspace
            expires_delta: Token expiration time delta
            
        Returns:
            JWT token string
        """
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

        expire = datetime.utcnow() + expires_delta
        
        payload = {
            "sub": str(user_id),
            "workspace_id": str(workspace_id),
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        
        encoded_jwt = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
        
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode and verify JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload
            
        Raises:
            UnauthorizedError: If token is invalid
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            raise UnauthorizedError("Token has expired")
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            raise UnauthorizedError("Invalid token")


class TokenData:
    """Decoded token data."""

    def __init__(self, user_id: str, workspace_id: str, role: str):
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.role = role
