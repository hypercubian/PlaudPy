"""Unit tests for Config API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.config_api import ConfigAPI
from plaudpy.config import PlaudConfig


@pytest.fixture
def config_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = ConfigAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestConfigAPI:

    def test_get_init_config(self, config_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"version": "1.0", "features": {"ai": True}}
        config_api.client.get.return_value = response

        result = config_api.get_init_config()

        assert result["version"] == "1.0"
        call_url = config_api.client.get.call_args[0][0]
        assert "/config/init" in call_url
