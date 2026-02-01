"""Unit tests for Tags API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.tags import TagsAPI
from plaudpy.config import PlaudConfig
from plaudpy.models.file import FileTag


@pytest.fixture
def tags_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = TagsAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestTagsAPI:

    def test_list_tags(self, tags_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "t1", "name": "Work", "color": "#ff0000"}]}
        tags_api.client.get.return_value = response

        result = tags_api.list_tags()

        assert len(result) == 1
        assert isinstance(result[0], FileTag)
        assert result[0].name == "Work"

    def test_create_tag(self, tags_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "t1", "name": "Meeting", "color": "#00ff00"}
        tags_api.client.post.return_value = response

        result = tags_api.create_tag("Meeting", color="#00ff00")

        assert isinstance(result, FileTag)
        assert result.name == "Meeting"
        call_url = tags_api.client.post.call_args[0][0]
        assert "/filetag/" in call_url

    def test_create_tag_without_color(self, tags_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "t1", "name": "Personal"}
        tags_api.client.post.return_value = response

        result = tags_api.create_tag("Personal")

        payload = tags_api.client.post.call_args[1]["json"]
        assert "color" not in payload

    def test_update_tag(self, tags_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "t1", "name": "Updated"}
        tags_api.client.patch.return_value = response

        result = tags_api.update_tag("t1", name="Updated")

        assert isinstance(result, FileTag)
        call_url = tags_api.client.patch.call_args[0][0]
        assert "/filetag/t1" in call_url

    def test_delete_tag(self, tags_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        tags_api.client.delete.return_value = response

        result = tags_api.delete_tag("t1")

        call_url = tags_api.client.delete.call_args[0][0]
        assert "/filetag/t1" in call_url
