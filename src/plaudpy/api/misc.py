"""Miscellaneous API endpoints."""

from .base import BaseAPI


class MiscAPI(BaseAPI):
    """API for miscellaneous operations."""

    def upload_info(self, **kwargs) -> dict:
        """Upload diagnostic or usage information.

        Args:
            **kwargs: Info payload fields.
        """
        return self._post("/others/upload-info", json=kwargs)
