"""Authentication tests."""

import pytest
from app.interfaces.auth import AuthUtils


def test_password_hashing():
    """Test password hashing and verification."""
    password = "TestPassword123!@"
    
    # Hash password
    hashed = AuthUtils.hash_password(password)
    
    # Verify it's different
    assert hashed != password
    
    # Verify correct password
    assert AuthUtils.verify_password(password, hashed)
    
    # Verify wrong password fails
    assert not AuthUtils.verify_password("WrongPassword", hashed)


def test_jwt_token_creation():
    """Test JWT token creation and decoding."""
    from uuid import uuid4
    
    user_id = uuid4()
    workspace_id = uuid4()
    role = "ADMIN"
    
    # Create token
    token = AuthUtils.create_access_token(user_id, workspace_id, role)
    
    # Decode token
    payload = AuthUtils.decode_token(token)
    
    # Verify payload
    assert payload["sub"] == str(user_id)
    assert payload["workspace_id"] == str(workspace_id)
    assert payload["role"] == role


def test_invalid_token():
    """Test decoding invalid token."""
    from app.core import UnauthorizedError
    
    invalid_token = "invalid.token.here"
    
    with pytest.raises(UnauthorizedError):
        AuthUtils.decode_token(invalid_token)
