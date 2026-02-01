"""Speakers API endpoints."""

from ..models.speaker import Speaker
from .base import BaseAPI


class SpeakersAPI(BaseAPI):
    """API for speaker profile operations."""

    def list_speakers(self) -> list[Speaker]:
        """List all speaker profiles."""
        data = self._get("/speaker/list")
        items = data if isinstance(data, list) else data.get("data", [])
        return [Speaker.model_validate(item) for item in items]

    def sync_speakers(self, speakers: list[dict]) -> dict:
        """Sync speaker profiles.

        Args:
            speakers: List of speaker data to sync.
        """
        return self._post("/speaker/sync", json=speakers)

    def delete_speaker(self, speaker_id: str) -> dict:
        """Delete a speaker profile.

        Args:
            speaker_id: Speaker ID to delete.
        """
        return self._delete(f"/speaker/{speaker_id}")
