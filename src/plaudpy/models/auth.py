"""Authentication models."""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Response from the authentication endpoint."""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int | None = None
    refresh_token: str | None = None
    scope: str | None = None


class AccessTokenInfo(BaseModel):
    """Information about an active access token."""

    model_config = {"extra": "allow"}

    id: str | None = None
    client_id: str | None = None
    created_at: str | None = None
    last_used: str | None = None


class SSOProvider(BaseModel):
    """SSO provider information."""

    model_config = {"extra": "allow"}

    provider: str | None = None
    name: str | None = None
    bound: bool | None = None
