"""Search-related models."""

from pydantic import BaseModel


class SearchResult(BaseModel):
    """A search result item."""

    model_config = {"extra": "allow"}

    id: str | None = None
    title: str | None = None
    snippet: str | None = None
    file_id: str | None = None


class SavedQuery(BaseModel):
    """A saved search query."""

    model_config = {"extra": "allow"}

    id: str | None = None
    query: str | None = None
    created_at: str | None = None
