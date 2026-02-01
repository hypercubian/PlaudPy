"""Tags API endpoints."""

from ..models.file import FileTag
from .base import BaseAPI


class TagsAPI(BaseAPI):
    """API for file tag CRUD operations."""

    def list_tags(self) -> list[FileTag]:
        """List all file tags."""
        data = self._get("/filetag/")
        items = data.get("data_filetag_list", data.get("data", []))
        if isinstance(data, list):
            items = data
        return [FileTag.model_validate(item) for item in items]

    def create_tag(self, name: str, color: str | None = None, icon: str | None = None) -> FileTag:
        """Create a new file tag.

        Args:
            name: Tag name.
            color: Optional tag color (hex string).
            icon: Optional icon code.
        """
        payload: dict = {"name": name}
        if color is not None:
            payload["color"] = color
        if icon is not None:
            payload["icon"] = icon
        data = self._post("/filetag/", json=payload)
        # Response wraps the tag in data_filetag when successful
        tag_data = data.get("data_filetag", data)
        return FileTag.model_validate(tag_data)

    def update_tag(self, tag_id: str, **kwargs) -> FileTag:
        """Update a file tag.

        Args:
            tag_id: Tag ID to update.
            **kwargs: Fields to update (name, color).
        """
        data = self._patch(f"/filetag/{tag_id}", json=kwargs)
        tag_data = data.get("data_filetag", data)
        return FileTag.model_validate(tag_data)

    def delete_tag(self, tag_id: str) -> dict:
        """Delete a file tag.

        Args:
            tag_id: Tag ID to delete.
        """
        return self._delete(f"/filetag/{tag_id}")
