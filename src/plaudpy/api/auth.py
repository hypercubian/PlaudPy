"""Authentication API."""

from ..exceptions import AuthenticationError
from ..models.auth import TokenResponse, AccessTokenInfo, SSOProvider
from .base import BaseAPI


class AuthAPI(BaseAPI):
    """Handle authentication with Plaud.ai."""

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
        import httpx

        url = f"{self.base_url}/auth/access-token"

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

    def list_tokens(self) -> list[AccessTokenInfo]:
        """List all active access tokens."""
        data = self._get("/auth/access-token/list")
        items = data if isinstance(data, list) else data.get("data", [])
        return [AccessTokenInfo.model_validate(item) for item in items]

    def logout(self) -> dict:
        """Logout and invalidate current access token."""
        return self._post("/auth/logout")

    def remove_token(self, token_id: str) -> dict:
        """Remove a specific access token.

        Args:
            token_id: ID of the token to remove.
        """
        return self._delete(f"/auth/access-token/{token_id}")

    def verify_magic_link(self, token: str) -> dict:
        """Verify a magic link login token.

        Args:
            token: The magic link token.
        """
        return self._post("/auth/magic-link/verify", json={"token": token})

    def list_sso_providers(self) -> list[SSOProvider]:
        """List available SSO providers."""
        data = self._get("/auth/sso/list")
        items = data if isinstance(data, list) else data.get("data", [])
        return [SSOProvider.model_validate(item) for item in items]

    def bind_sso(self, provider: str, **kwargs) -> dict:
        """Bind an SSO provider to the account.

        Args:
            provider: SSO provider identifier.
            **kwargs: Additional provider-specific parameters.
        """
        payload = {"provider": provider, **kwargs}
        return self._post("/auth/sso/bindAccount", json=payload)

    def unbind_sso(self, provider: str) -> dict:
        """Unbind an SSO provider from the account.

        Args:
            provider: SSO provider identifier.
        """
        return self._post("/auth/sso/unBindAccount", json={"provider": provider})
