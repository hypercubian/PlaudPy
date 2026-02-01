"""Speaker-related models."""

from pydantic import BaseModel


class Speaker(BaseModel):
    """A speaker profile."""

    model_config = {"extra": "allow"}

    id: str | None = None
    name: str | None = None
    avatar: str | None = None
