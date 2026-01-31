"""Custom exceptions for PlaudPy."""


class PlaudError(Exception):
    """Base exception for PlaudPy errors."""

    pass


class AuthenticationError(PlaudError):
    """Raised when authentication fails."""

    pass


class APIError(PlaudError):
    """Raised when an API request fails."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class ConfigurationError(PlaudError):
    """Raised when configuration is invalid or missing."""

    pass
