"""Unit tests for Devices API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.devices import DevicesAPI
from plaudpy.config import PlaudConfig
from plaudpy.models.device import Device


@pytest.fixture
def devices_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = DevicesAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestDevicesAPI:

    def test_list_devices(self, devices_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {
            "data": [
                {"id": "d1", "name": "My Plaud Note", "model": "PN-1", "firmware_version": "2.1.0"}
            ]
        }
        devices_api.client.get.return_value = response

        result = devices_api.list_devices()

        assert len(result) == 1
        assert isinstance(result[0], Device)
        assert result[0].name == "My Plaud Note"
        assert result[0].model == "PN-1"
        call_url = devices_api.client.get.call_args[0][0]
        assert "/device/list" in call_url

    def test_list_devices_empty(self, devices_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": []}
        devices_api.client.get.return_value = response

        result = devices_api.list_devices()
        assert result == []
