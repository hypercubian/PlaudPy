"""Authentication models."""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Response from the authentication endpoint."""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int | None = None
    refresh_token: str | None = None
    scope: str | None = None
