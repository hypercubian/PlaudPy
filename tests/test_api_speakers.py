"""Unit tests for Speakers API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.speakers import SpeakersAPI
from plaudpy.config import PlaudConfig
from plaudpy.models.speaker import Speaker


@pytest.fixture
def speakers_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = SpeakersAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestSpeakersAPI:

    def test_list_speakers(self, speakers_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "s1", "name": "Alice"}, {"id": "s2", "name": "Bob"}]}
        speakers_api.client.get.return_value = response

        result = speakers_api.list_speakers()

        assert len(result) == 2
        assert isinstance(result[0], Speaker)
        assert result[0].name == "Alice"
        call_url = speakers_api.client.get.call_args[0][0]
        assert "/speaker/list" in call_url

    def test_sync_speakers(self, speakers_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"synced": 2}
        speakers_api.client.post.return_value = response

        result = speakers_api.sync_speakers([{"name": "Alice"}, {"name": "Bob"}])

        call_url = speakers_api.client.post.call_args[0][0]
        assert "/speaker/sync" in call_url

    def test_delete_speaker(self, speakers_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        speakers_api.client.delete.return_value = response

        result = speakers_api.delete_speaker("s1")

        call_url = speakers_api.client.delete.call_args[0][0]
        assert "/speaker/s1" in call_url
