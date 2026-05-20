"""
Custom application exceptions.
Each exception carries an HTTP-friendly status code so that the API layer
can translate domain errors into proper HTTP responses.
"""


class AppBaseError(Exception):
    """Base class for all application exceptions."""

    status_code: int = 500

    def __init__(self, detail: str = "An unexpected error occurred") -> None:
        self.detail = detail
        super().__init__(self.detail)


class NotFoundError(AppBaseError):
    """Raised when a requested resource does not exist."""

    status_code = 404

    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(detail=detail)


class UnauthorizedError(AppBaseError):
    """Raised when authentication fails or credentials are invalid."""

    status_code = 401

    def __init__(self, detail: str = "Invalid credentials") -> None:
        super().__init__(detail=detail)


class ForbiddenError(AppBaseError):
    """Raised when the user lacks permission for the requested action."""

    status_code = 403

    def __init__(self, detail: str = "Permission denied") -> None:
        super().__init__(detail=detail)


class ConflictError(AppBaseError):
    """Raised when an operation conflicts with existing state (e.g. duplicate)."""

    status_code = 409

    def __init__(self, detail: str = "Resource already exists") -> None:
        super().__init__(detail=detail)


class ValidationError(AppBaseError):
    """Raised when input data fails domain-level validation."""

    status_code = 422

    def __init__(self, detail: str = "Validation failed") -> None:
        super().__init__(detail=detail)

class DatabaseError(AppBaseError):
    """Raised when database operation fails."""

    status_code = 500

    def __init__(self, detail: str = "Database operation failed") -> None:
        super().__init__(detail=detail)

