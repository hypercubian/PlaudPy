"""Authentication API."""

import httpx

from ..config import PlaudConfig
from ..exceptions import AuthenticationError
from ..models import TokenResponse


class AuthAPI:
    """Handle authentication with Plaud.ai."""

    def __init__(self, config: PlaudConfig, http_client: httpx.Client):
        self.config = config
        self.client = http_client

    def login(self, username: str, password: str) -> TokenResponse:
        """Authenticate and get access token.

        Args:
            username: Plaud account email.
            password: Plaud account password.

        Returns:
            TokenResponse with access token.

        Raises:
            AuthenticationError: If authentication fails.
        """
        url = f"{self.config.base_url}/auth/access-token"

        # Auth endpoint expects multipart form data
        data = {
            "username": username,
            "password": password,
            "client_id": self.config.client_id,
        }

        try:
            response = self.client.post(url, data=data)

            if response.status_code == 401:
                raise AuthenticationError("Invalid username or password")

            if response.status_code >= 400:
                raise AuthenticationError(f"Authentication failed: {response.text}")

            return TokenResponse.model_validate(response.json())

        except httpx.RequestError as e:
            raise AuthenticationError(f"Request failed: {e}")
