"""Unit tests for PlaudClient with mocked HTTP responses."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from plaudpy import PlaudClient
from plaudpy.exceptions import AuthenticationError, ConfigurationError


class TestPlaudClientInit:
    """Tests for PlaudClient initialization."""

    def test_missing_credentials_raises_error(self):
        """Should raise ConfigurationError when no credentials provided."""
        # Need to patch the config to simulate missing credentials
        with patch("plaudpy.client.PlaudConfig") as mock_config_class:
            mock_config = MagicMock()
            mock_config.username = None
            mock_config.password = None
            mock_config_class.return_value = mock_config

            with pytest.raises(ConfigurationError) as exc_info:
                PlaudClient()
            assert "Credentials required" in str(exc_info.value)

    def test_accepts_explicit_credentials(self, sample_files_response, sample_file_details_response):
        """Should accept username/password passed to constructor."""
        with patch("httpx.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            # Mock auth response
            auth_response = MagicMock()
            auth_response.status_code = 200
            auth_response.json.return_value = {"access_token": "test-token"}

            mock_client.post.return_value = auth_response

            client = PlaudClient(username="test@example.com", password="secret")
            assert client.config.username == "test@example.com"
            assert client.config.password == "secret"


class TestPlaudClientMocked:
    """Tests for PlaudClient with mocked API responses."""

    @pytest.fixture
    def mock_http_client(self):
        """Create a mock HTTP client."""
        return MagicMock(spec=httpx.Client)

    @pytest.fixture
    def client_with_mocks(self, mock_http_client, sample_files_response, sample_file_details_response):
        """Create a PlaudClient with mocked HTTP responses."""
        # Setup auth response
        auth_response = MagicMock()
        auth_response.status_code = 200
        auth_response.json.return_value = {"access_token": "test-token"}

        # Setup files responses
        files_response = MagicMock()
        files_response.status_code = 200
        files_response.json.return_value = sample_files_response

        details_response = MagicMock()
        details_response.status_code = 200
        details_response.json.return_value = sample_file_details_response

        def mock_post(url, **kwargs):
            if "access-token" in url:
                return auth_response
            elif "file/list" in url:
                return details_response
            return MagicMock(status_code=200, json=lambda: {})

        def mock_get(url, **kwargs):
            if "simple/web" in url:
                return files_response
            return MagicMock(status_code=200, json=lambda: {})

        mock_http_client.post.side_effect = mock_post
        mock_http_client.get.side_effect = mock_get

        with patch("httpx.Client", return_value=mock_http_client):
            client = PlaudClient(username="test@example.com", password="secret")
            return client

    def test_get_recordings(self, client_with_mocks):
        """Should return list of Recording objects."""
        recordings = client_with_mocks.get_recordings()

        assert len(recordings) == 1
        assert recordings[0].id == "abc123"
        assert recordings[0].title == "Test Recording"

    def test_get_recordings_includes_transcript(self, client_with_mocks):
        """Recordings should include parsed transcripts."""
        recordings = client_with_mocks.get_recordings()

        assert len(recordings[0].transcript.entries) == 3
        assert recordings[0].transcript.entries[0].speaker == "Speaker 1"

    def test_get_recordings_includes_summary(self, client_with_mocks):
        """Recordings should include summary."""
        recordings = client_with_mocks.get_recordings()

        assert recordings[0].summary == "This is a summary of the meeting."


class TestAuthenticationErrors:
    """Tests for authentication error handling."""

    def test_invalid_credentials_raises_error(self):
        """Should raise AuthenticationError on 401 response."""
        with patch("httpx.Client") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            # Mock 401 response
            auth_response = MagicMock()
            auth_response.status_code = 401
            auth_response.text = "Invalid credentials"

            mock_client.post.return_value = auth_response

            with pytest.raises(AuthenticationError) as exc_info:
                PlaudClient(username="bad@example.com", password="wrong")

            assert "Invalid username or password" in str(exc_info.value)
