"""Unit tests for Auth API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.auth import AuthAPI
from plaudpy.config import PlaudConfig
from plaudpy.exceptions import AuthenticationError
from plaudpy.models.auth import AccessTokenInfo, SSOProvider, TokenResponse


@pytest.fixture
def auth_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = AuthAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestAuthAPI:

    def test_login_success(self, auth_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"access_token": "new-token", "token_type": "Bearer"}
        auth_api.client.post.return_value = response

        result = auth_api.login("user@example.com", "password123")

        assert isinstance(result, TokenResponse)
        assert result.access_token == "new-token"

    def test_login_invalid_credentials(self, auth_api):
        response = MagicMock(status_code=401)
        response.text = "Invalid credentials"
        auth_api.client.post.return_value = response

        with pytest.raises(AuthenticationError, match="Invalid username or password"):
            auth_api.login("bad@example.com", "wrong")

    def test_login_server_error(self, auth_api):
        response = MagicMock(status_code=500)
        response.text = "Internal Server Error"
        auth_api.client.post.return_value = response

        with pytest.raises(AuthenticationError, match="Authentication failed"):
            auth_api.login("user@example.com", "password")

    def test_list_tokens(self, auth_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "tok1", "client_id": "web"}]}
        auth_api.client.get.return_value = response

        result = auth_api.list_tokens()

        assert len(result) == 1
        assert isinstance(result[0], AccessTokenInfo)
        assert result[0].client_id == "web"

    def test_logout(self, auth_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        auth_api.client.post.return_value = response

        result = auth_api.logout()

        call_url = auth_api.client.post.call_args[0][0]
        assert "/auth/logout" in call_url

    def test_remove_token(self, auth_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        auth_api.client.delete.return_value = response

        result = auth_api.remove_token("tok1")

        call_url = auth_api.client.delete.call_args[0][0]
        assert "/auth/access-token/tok1" in call_url

    def test_verify_magic_link(self, auth_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"verified": True}
        auth_api.client.post.return_value = response

        result = auth_api.verify_magic_link("magic-token-123")

        call_url = auth_api.client.post.call_args[0][0]
        assert "/auth/magic-link/verify" in call_url

    def test_list_sso_providers(self, auth_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"provider": "google", "name": "Google", "bound": True}]}
        auth_api.client.get.return_value = response

        result = auth_api.list_sso_providers()

        assert len(result) == 1
        assert isinstance(result[0], SSOProvider)
        assert result[0].provider == "google"

    def test_bind_sso(self, auth_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"status": "bound"}
        auth_api.client.post.return_value = response

        result = auth_api.bind_sso("google", token="google-token")

        call_url = auth_api.client.post.call_args[0][0]
        assert "/auth/sso/bindAccount" in call_url

    def test_unbind_sso(self, auth_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"status": "unbound"}
        auth_api.client.post.return_value = response

        result = auth_api.unbind_sso("google")

        call_url = auth_api.client.post.call_args[0][0]
        assert "/auth/sso/unBindAccount" in call_url
