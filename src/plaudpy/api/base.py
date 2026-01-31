"""Base API class with common functionality."""

import httpx

from ..config import PlaudConfig
from ..exceptions import APIError


class BaseAPI:
    """Base class for API endpoints with authentication handling."""

    def __init__(self, config: PlaudConfig, http_client: httpx.Client):
        self.config = config
        self.client = http_client
        self._access_token: str | None = None

    @property
    def base_url(self) -> str:
        return self.config.base_url

    @property
    def headers(self) -> dict[str, str]:
        """Get headers for authenticated requests."""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        return headers

    def set_access_token(self, token: str) -> None:
        """Set the access token for authenticated requests."""
        self._access_token = token

    def _handle_response(self, response: httpx.Response) -> dict:
        """Handle API response and raise errors if needed."""
        if response.status_code >= 400:
            try:
                error_data = response.json()
                message = error_data.get("message", response.text)
            except Exception:
                message = response.text
            raise APIError(message, status_code=response.status_code)

        if response.status_code == 204:
            return {}

        return response.json()
