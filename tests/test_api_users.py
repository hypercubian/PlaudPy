"""Unit tests for Users API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.users import UsersAPI
from plaudpy.config import PlaudConfig
from plaudpy.models.user import (
    FeatureAccess,
    FileStats,
    TranscriptionQuota,
    UserProfile,
    UserSettings,
)


@pytest.fixture
def users_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = UsersAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestUsersAPI:

    def test_get_me(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "u1", "email": "test@example.com", "nickname": "Test User"}
        users_api.client.get.return_value = response

        result = users_api.get_me()

        assert isinstance(result, UserProfile)
        assert result.email == "test@example.com"
        call_url = users_api.client.get.call_args[0][0]
        assert "/user/me" in call_url

    def test_get_settings(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"theme": "dark"}
        users_api.client.get.return_value = response

        result = users_api.get_settings()
        assert isinstance(result, UserSettings)

    def test_update_settings(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"theme": "light"}
        users_api.client.post.return_value = response

        result = users_api.update_settings(theme="light")

        assert isinstance(result, UserSettings)
        call_url = users_api.client.post.call_args[0][0]
        assert "/user/me/settings" in call_url

    def test_get_transactions(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": []}
        users_api.client.get.return_value = response

        result = users_api.get_transactions()

        call_url = users_api.client.get.call_args[0][0]
        assert "/user/me/history/transactions" in call_url

    def test_get_transcript_history(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": []}
        users_api.client.get.return_value = response

        result = users_api.get_transcript_history()

        call_url = users_api.client.get.call_args[0][0]
        assert "/user/me/history/transcripts" in call_url

    def test_get_pcs_status_list(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": []}
        users_api.client.get.return_value = response

        result = users_api.get_pcs_status_list()

        call_url = users_api.client.get.call_args[0][0]
        assert "/user/me/pcs-status-list" in call_url

    def test_query(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": {}}
        users_api.client.get.return_value = response

        result = users_api.query(field="name")

        call_url = users_api.client.get.call_args[0][0]
        assert "/user/me/query" in call_url

    def test_get_file_stats(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"total_files": 42, "total_duration": 3600}
        users_api.client.get.return_value = response

        result = users_api.get_file_stats()

        assert isinstance(result, FileStats)
        assert result.total_files == 42

    def test_get_transcription_quota(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"total": 300, "used": 100, "remaining": 200}
        users_api.client.get.return_value = response

        result = users_api.get_transcription_quota()

        assert isinstance(result, TranscriptionQuota)
        assert result.total == 300
        assert result.remaining == 200

    def test_set_quota_notification(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"enabled": True}
        users_api.client.post.return_value = response

        result = users_api.set_quota_notification(enabled=True)

        call_url = users_api.client.post.call_args[0][0]
        assert "/user/stat/transcription/quota/notification" in call_url

    def test_get_feature_access(self, users_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"premium": True}
        users_api.client.get.return_value = response

        result = users_api.get_feature_access()
        assert isinstance(result, FeatureAccess)
