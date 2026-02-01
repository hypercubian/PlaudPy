"""Main PlaudClient class."""

from pathlib import Path

import httpx

from .api.ai import AIAPI
from .api.auth import AuthAPI
from .api.config_api import ConfigAPI
from .api.devices import DevicesAPI
from .api.files import FilesAPI
from .api.membership import MembershipAPI
from .api.misc import MiscAPI
from .api.search import SearchAPI
from .api.speakers import SpeakersAPI
from .api.tags import TagsAPI
from .api.templates import TemplatesAPI
from .api.users import UsersAPI
from .config import PlaudConfig
from .exceptions import ConfigurationError
from .models import Recording, SearchResult, UserProfile, TranscriptionQuota


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

        # Access sub-APIs directly
        client.users.get_me()
        client.ai.get_task_status()
        client.speakers.list_speakers()
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
            base_url: API base URL. Defaults to https://api.plaud.ai.
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

        # Initialize all API modules
        self._auth_api = AuthAPI(self.config, self._http_client)
        self._files_api = FilesAPI(self.config, self._http_client)
        self._ai_api = AIAPI(self.config, self._http_client)
        self._users_api = UsersAPI(self.config, self._http_client)
        self._tags_api = TagsAPI(self.config, self._http_client)
        self._speakers_api = SpeakersAPI(self.config, self._http_client)
        self._search_api = SearchAPI(self.config, self._http_client)
        self._templates_api = TemplatesAPI(self.config, self._http_client)
        self._membership_api = MembershipAPI(self.config, self._http_client)
        self._config_api = ConfigAPI(self.config, self._http_client)
        self._devices_api = DevicesAPI(self.config, self._http_client)
        self._misc_api = MiscAPI(self.config, self._http_client)

        # Collect all APIs for token distribution
        self._apis = [
            self._auth_api,
            self._files_api,
            self._ai_api,
            self._users_api,
            self._tags_api,
            self._speakers_api,
            self._search_api,
            self._templates_api,
            self._membership_api,
            self._config_api,
            self._devices_api,
            self._misc_api,
        ]

        # Authenticate
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with the API and distribute token to all sub-APIs."""
        token_response = self._auth_api.login(
            self.config.username,  # type: ignore
            self.config.password,  # type: ignore
        )
        for api in self._apis:
            api.set_access_token(token_response.access_token)

    # --- Sub-API properties ---

    @property
    def auth(self) -> AuthAPI:
        """Authentication API (token management, SSO)."""
        return self._auth_api

    @property
    def files(self) -> FilesAPI:
        """Files API (list, detail, download, upload, trash)."""
        return self._files_api

    @property
    def ai(self) -> AIAPI:
        """AI API (transcription, summarization, templates, labels)."""
        return self._ai_api

    @property
    def users(self) -> UsersAPI:
        """Users API (profile, settings, stats, quota)."""
        return self._users_api

    @property
    def tags(self) -> TagsAPI:
        """Tags API (CRUD for file tags)."""
        return self._tags_api

    @property
    def speakers(self) -> SpeakersAPI:
        """Speakers API (list, sync, delete)."""
        return self._speakers_api

    @property
    def search(self) -> SearchAPI:
        """Search API (search recordings, saved queries)."""
        return self._search_api

    @property
    def templates(self) -> TemplatesAPI:
        """Templates API (built-in and community templates)."""
        return self._templates_api

    @property
    def membership(self) -> MembershipAPI:
        """Membership API (subscriptions, billing)."""
        return self._membership_api

    @property
    def app_config(self) -> ConfigAPI:
        """Config API (application configuration)."""
        return self._config_api

    @property
    def devices(self) -> DevicesAPI:
        """Devices API (list registered devices)."""
        return self._devices_api

    @property
    def misc(self) -> MiscAPI:
        """Miscellaneous API."""
        return self._misc_api

    # --- Convenience methods ---

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

    def trigger_transcription(self, file_id: str, **kwargs) -> dict:
        """Trigger transcription/summarization for a file.

        Args:
            file_id: The file ID to process.
            **kwargs: Additional transcription options.

        Returns:
            API response data.
        """
        return self._ai_api.trigger_transcription(file_id, **kwargs)

    def get_me(self) -> UserProfile:
        """Get the current user's profile."""
        return self._users_api.get_me()

    def get_quota(self) -> TranscriptionQuota:
        """Get transcription quota information."""
        return self._users_api.get_transcription_quota()

    def download_recording(self, file_id: str, path: str | Path) -> Path:
        """Download a recording's audio to disk.

        Args:
            file_id: The file ID to download.
            path: Destination file path.

        Returns:
            Path to the downloaded file.
        """
        path = Path(path)
        content = self._files_api.download(file_id)
        path.write_bytes(content)
        return path

    def search_recordings(self, query: str, **kwargs) -> list[SearchResult]:
        """Search recordings.

        Args:
            query: Search query string.
            **kwargs: Additional search parameters.

        Returns:
            List of SearchResult objects.
        """
        return self._search_api.search(query, **kwargs)

    def close(self) -> None:
        """Close the HTTP client."""
        self._http_client.close()

    def __enter__(self) -> "PlaudClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
