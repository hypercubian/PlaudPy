"""Unit tests for Misc API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.misc import MiscAPI
from plaudpy.config import PlaudConfig


@pytest.fixture
def misc_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = MiscAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestMiscAPI:

    def test_upload_info(self, misc_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"status": "ok"}
        misc_api.client.post.return_value = response

        result = misc_api.upload_info(event="app_open", platform="web")

        call_url = misc_api.client.post.call_args[0][0]
        assert "/others/upload-info" in call_url
        assert result["status"] == "ok"
