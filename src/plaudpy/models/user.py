"""User-related models."""

from pydantic import BaseModel


class UserProfile(BaseModel):
    """User profile information."""

    model_config = {"extra": "allow"}

    id: str | None = None
    email: str | None = None
    username: str | None = None
    nickname: str | None = None
    avatar: str | None = None
    created_at: str | None = None


class UserSettings(BaseModel):
    """User settings."""

    model_config = {"extra": "allow"}


class FileStats(BaseModel):
    """File statistics for the user."""

    model_config = {"extra": "allow"}

    total_files: int | None = None
    total_duration: int | None = None


class TranscriptionQuota(BaseModel):
    """Transcription quota information."""

    model_config = {"extra": "allow"}

    total: int | None = None
    used: int | None = None
    remaining: int | None = None


class FeatureAccess(BaseModel):
    """Feature access information."""

    model_config = {"extra": "allow"}
