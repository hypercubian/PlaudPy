"""Template-related models."""

from pydantic import BaseModel


class SummaryTemplate(BaseModel):
    """A summary template (built-in or community)."""

    model_config = {"extra": "allow"}

    id: str | None = None
    name: str | None = None
    prompt: str | None = None
    description: str | None = None
    category: str | None = None
    is_system: bool | None = None
    author: str | None = None
    likes: int | None = None


class TemplateCategory(BaseModel):
    """A template category."""

    model_config = {"extra": "allow"}

    id: str | None = None
    name: str | None = None
    description: str | None = None
