"""AI-related models."""

from pydantic import BaseModel


class TaskStatus(BaseModel):
    """Status of an AI processing task."""

    model_config = {"extra": "allow"}

    file_id: str | None = None
    status: str | None = None
    progress: float | None = None


class CustomTemplate(BaseModel):
    """A custom AI summary template."""

    model_config = {"extra": "allow"}

    id: str | None = None
    name: str | None = None
    prompt: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
