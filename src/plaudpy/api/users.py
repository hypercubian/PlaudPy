"""Users API endpoints."""

from ..models.user import (
    FeatureAccess,
    FileStats,
    TranscriptionQuota,
    UserProfile,
    UserSettings,
)
from .base import BaseAPI


class UsersAPI(BaseAPI):
    """API for user profile, settings, and stats."""

    def get_me(self) -> UserProfile:
        """Get the current user's profile."""
        data = self._get("/user/me")
        return UserProfile.model_validate(data)

    def get_settings(self) -> UserSettings:
        """Get the current user's settings."""
        data = self._get("/user/me/settings")
        return UserSettings.model_validate(data)

    def update_settings(self, **kwargs) -> UserSettings:
        """Update user settings.

        Args:
            **kwargs: Settings to update.
        """
        data = self._post("/user/me/settings", json=kwargs)
        return UserSettings.model_validate(data)

    def get_transactions(self, **kwargs) -> dict:
        """Get the user's transaction history.

        Args:
            **kwargs: Query parameters (e.g. skip, limit).
        """
        return self._get("/user/me/history/transactions", params=kwargs or None)

    def get_transcript_history(self, **kwargs) -> dict:
        """Get the user's transcript processing history.

        Args:
            **kwargs: Query parameters (e.g. skip, limit).
        """
        return self._get("/user/me/history/transcripts", params=kwargs or None)

    def get_pcs_status_list(self) -> dict:
        """Get the user's PCS status list."""
        return self._get("/user/me/pcs-status-list")

    def query(self, **kwargs) -> dict:
        """Query user information.

        Args:
            **kwargs: Query parameters.
        """
        return self._get("/user/me/query", params=kwargs or None)

    def get_file_stats(self) -> FileStats:
        """Get file statistics for the user."""
        data = self._get("/user/stat/file")
        return FileStats.model_validate(data)

    def get_transcription_quota(self) -> TranscriptionQuota:
        """Get transcription quota information."""
        data = self._get("/user/stat/transcription/quota")
        return TranscriptionQuota.model_validate(data)

    def set_quota_notification(self, **kwargs) -> dict:
        """Set quota notification preferences.

        Args:
            **kwargs: Notification settings.
        """
        return self._post("/user/stat/transcription/quota/notification", json=kwargs)

    def get_feature_access(self) -> FeatureAccess:
        """Get feature access information for the user."""
        data = self._get("/user/feature-access")
        return FeatureAccess.model_validate(data)
