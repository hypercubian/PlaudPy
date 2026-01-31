"""Main PlaudClient class."""

import httpx

from .api.auth import AuthAPI
from .api.files import FilesAPI
from .config import PlaudConfig
from .exceptions import ConfigurationError
from .models import Recording


class PlaudClient:
    """Client for interacting with the Plaud.ai API.

    Example:
        # Using environment variables (PLAUD_USERNAME, PLAUD_PASSWORD)
        client = PlaudClient()

        # Or explicit credentials
        client = PlaudClient(username="email@example.com", password="secret")

        # Get all recordings
        for recording in client.get_recordings():
            print(recording.title)
            print(recording.summary)
    """

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        base_url: str | None = None,
    ):
        """Initialize the Plaud client.

        Args:
            username: Plaud account email. Defaults to PLAUD_USERNAME env var.
            password: Plaud account password. Defaults to PLAUD_PASSWORD env var.
            base_url: API base URL. Defaults to https://app.plaud.ai.
        """
        self.config = PlaudConfig()

        # Override config with explicit values
        if username:
            self.config.username = username
        if password:
            self.config.password = password
        if base_url:
            self.config.base_url = base_url

        # Validate credentials
        if not self.config.username or not self.config.password:
            raise ConfigurationError(
                "Credentials required. Set PLAUD_USERNAME and PLAUD_PASSWORD "
                "environment variables or pass username/password to constructor."
            )

        # Initialize HTTP client
        self._http_client = httpx.Client(timeout=30.0)

        # Initialize APIs
        self._auth_api = AuthAPI(self.config, self._http_client)
        self._files_api = FilesAPI(self.config, self._http_client)

        # Authenticate
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with the API."""
        token_response = self._auth_api.login(
            self.config.username,  # type: ignore
            self.config.password,  # type: ignore
        )
        self._files_api.set_access_token(token_response.access_token)

    def get_recordings(self) -> list[Recording]:
        """Get all recordings with transcripts and summaries.

        Returns:
            List of Recording objects.
        """
        # First get simple list to get all file IDs
        simple_files = self._files_api.list_simple()
        file_ids = [f.id for f in simple_files]

        if not file_ids:
            return []

        # Get detailed info including transcripts
        details = self._files_api.get_details(file_ids)

        return [Recording.from_file_detail(d) for d in details]

    def get_recording(self, file_id: str) -> Recording | None:
        """Get a single recording by ID.

        Args:
            file_id: The file ID to fetch.

        Returns:
            Recording object or None if not found.
        """
        details = self._files_api.get_details([file_id])
        if not details:
            return None
        return Recording.from_file_detail(details[0])

    def trigger_transcription(self, file_id: str) -> dict:
        """Trigger transcription/summarization for a file.

        Args:
            file_id: The file ID to process.

        Returns:
            API response data.
        """
        return self._files_api.trigger_transcription(file_id)

    def close(self) -> None:
        """Close the HTTP client."""
        self._http_client.close()

    def __enter__(self) -> "PlaudClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
