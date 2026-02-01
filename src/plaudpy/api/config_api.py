"""Config API endpoints."""

from .base import BaseAPI


class ConfigAPI(BaseAPI):
    """API for application configuration."""

    def get_init_config(self) -> dict:
        """Get initial application configuration."""
        return self._get("/config/init")
