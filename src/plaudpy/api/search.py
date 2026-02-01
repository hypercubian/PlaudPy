"""Search API endpoints."""

from ..models.search import SavedQuery, SearchResult
from .base import BaseAPI


class SearchAPI(BaseAPI):
    """API for search operations."""

    def search(self, query: str, **kwargs) -> list[SearchResult]:
        """Search recordings.

        Args:
            query: Search query string.
            **kwargs: Additional search parameters.
        """
        payload = {"query": query, **kwargs}
        data = self._post("/gsearch/v1/search", json=payload)
        items = data if isinstance(data, list) else data.get("data", data.get("results", []))
        return [SearchResult.model_validate(item) for item in items]

    def list_saved_queries(self) -> list[SavedQuery]:
        """List saved search queries."""
        data = self._get("/gsearch/v1/saved-queries")
        items = data if isinstance(data, list) else data.get("data", [])
        return [SavedQuery.model_validate(item) for item in items]

    def create_saved_query(self, query: str) -> SavedQuery:
        """Save a search query.

        Args:
            query: Search query to save.
        """
        data = self._post("/gsearch/v1/saved-queries", json={"query": query})
        return SavedQuery.model_validate(data)

    def delete_saved_query(self, query_id: str) -> dict:
        """Delete a saved search query.

        Args:
            query_id: Saved query ID to delete.
        """
        return self._delete(f"/gsearch/v1/saved-queries/{query_id}")
