"""Templates API endpoints."""

from ..models.template import SummaryTemplate, TemplateCategory
from .base import BaseAPI


class TemplatesAPI(BaseAPI):
    """API for summary template operations (built-in and community)."""

    # --- Built-in templates ---

    def list_chatllm_templates(self) -> list[SummaryTemplate]:
        """List built-in ChatLLM summary templates."""
        data = self._get("/chatllm-template/list")
        items = data if isinstance(data, list) else data.get("data", [])
        return [SummaryTemplate.model_validate(item) for item in items]

    def get_recommended_templates(self) -> list[SummaryTemplate]:
        """Get recommended summary templates."""
        data = self._get("/chatllm-template/recommended")
        items = data if isinstance(data, list) else data.get("data", [])
        return [SummaryTemplate.model_validate(item) for item in items]

    def get_template_categories(self) -> list[TemplateCategory]:
        """Get template categories."""
        data = self._get("/chatllm-template/categories")
        items = data if isinstance(data, list) else data.get("data", [])
        return [TemplateCategory.model_validate(item) for item in items]

    # --- Community templates ---

    def search_community_templates(self, query: str = "", **kwargs) -> list[SummaryTemplate]:
        """Search community templates.

        Args:
            query: Search query.
            **kwargs: Additional filter parameters.
        """
        payload = {"query": query, **kwargs}
        data = self._post("/community-template/search", json=payload)
        items = data if isinstance(data, list) else data.get("data", [])
        return [SummaryTemplate.model_validate(item) for item in items]

    def create_community_template(self, name: str, prompt: str, **kwargs) -> SummaryTemplate:
        """Create a community template.

        Args:
            name: Template name.
            prompt: Template prompt text.
            **kwargs: Additional fields (description, category).
        """
        payload = {"name": name, "prompt": prompt, **kwargs}
        data = self._post("/community-template/create", json=payload)
        return SummaryTemplate.model_validate(data)

    def edit_community_template(self, template_id: str, **kwargs) -> SummaryTemplate:
        """Edit a community template.

        Args:
            template_id: Template ID.
            **kwargs: Fields to update.
        """
        data = self._patch(f"/community-template/{template_id}", json=kwargs)
        return SummaryTemplate.model_validate(data)

    def delete_community_template(self, template_id: str) -> dict:
        """Delete a community template.

        Args:
            template_id: Template ID to delete.
        """
        return self._delete(f"/community-template/{template_id}")

    def favorite_template(self, template_id: str) -> dict:
        """Add a template to favorites.

        Args:
            template_id: Template ID to favorite.
        """
        return self._post(f"/community-template/{template_id}/favorite")

    def unfavorite_template(self, template_id: str) -> dict:
        """Remove a template from favorites.

        Args:
            template_id: Template ID to unfavorite.
        """
        return self._post(f"/community-template/{template_id}/unfavorite")

    def list_favorite_templates(self) -> list[SummaryTemplate]:
        """List favorited community templates."""
        data = self._get("/community-template/favorites")
        items = data if isinstance(data, list) else data.get("data", [])
        return [SummaryTemplate.model_validate(item) for item in items]

    def get_community_home(self) -> dict:
        """Get community template home page data."""
        return self._get("/community-template/home")

    def list_my_templates(self) -> list[SummaryTemplate]:
        """List the current user's community templates."""
        data = self._get("/community-template/mine")
        items = data if isinstance(data, list) else data.get("data", [])
        return [SummaryTemplate.model_validate(item) for item in items]

    def list_recently_used(self) -> list[SummaryTemplate]:
        """List recently used templates."""
        data = self._get("/community-template/recently-used")
        items = data if isinstance(data, list) else data.get("data", [])
        return [SummaryTemplate.model_validate(item) for item in items]

    def get_daily_recommendations(self) -> list[SummaryTemplate]:
        """Get daily template recommendations."""
        data = self._get("/community-template/daily-recommendations")
        items = data if isinstance(data, list) else data.get("data", [])
        return [SummaryTemplate.model_validate(item) for item in items]

    def get_weekly_recommendations(self) -> list[SummaryTemplate]:
        """Get weekly template recommendations."""
        data = self._get("/community-template/weekly-recommendations")
        items = data if isinstance(data, list) else data.get("data", [])
        return [SummaryTemplate.model_validate(item) for item in items]
