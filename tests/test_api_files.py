"""Unit tests for Files API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.files import FilesAPI
from plaudpy.config import PlaudConfig
from plaudpy.models.file import FileDetail, FileSimple, UploadPresignedUrl


@pytest.fixture
def files_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = FilesAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestFilesAPI:

    def test_list_simple(self, files_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {
            "data_file_list": [
                {"id": "f1", "filename": "Test", "duration": 60, "start_time": 1700000000000}
            ]
        }
        files_api.client.get.return_value = response

        result = files_api.list_simple()

        assert len(result) == 1
        assert isinstance(result[0], FileSimple)
        assert result[0].id == "f1"

    def test_get_details(self, files_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {
            "data_file_list": [
                {"id": "f1", "filename": "Test", "duration": 60, "start_time": 1700000000000}
            ]
        }
        files_api.client.post.return_value = response

        result = files_api.get_details(["f1"])

        assert len(result) == 1
        assert isinstance(result[0], FileDetail)

    def test_get_details_empty(self, files_api):
        result = files_api.get_details([])
        assert result == []

    def test_get_detail(self, files_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "f1", "filename": "Test", "duration": 60, "start_time": 0}
        files_api.client.get.return_value = response

        result = files_api.get_detail("f1")

        assert isinstance(result, FileDetail)
        call_url = files_api.client.get.call_args[0][0]
        assert "/file/detail/f1" in call_url

    def test_download(self, files_api):
        response = MagicMock(status_code=200)
        response.content = b"audio-data-bytes"
        files_api.client.get.return_value = response

        result = files_api.download("f1")

        assert result == b"audio-data-bytes"
        call_url = files_api.client.get.call_args[0][0]
        assert "/file/download/f1" in call_url

    def test_update(self, files_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "f1", "filename": "Renamed"}
        files_api.client.patch.return_value = response

        result = files_api.update("f1", filename="Renamed")

        call_url = files_api.client.patch.call_args[0][0]
        assert "/file/f1" in call_url

    def test_trash(self, files_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        files_api.client.post.return_value = response

        result = files_api.trash(["f1", "f2"])

        call_url = files_api.client.post.call_args[0][0]
        assert "/file/trash/" in call_url
        call_json = files_api.client.post.call_args[1]["json"]
        assert call_json == ["f1", "f2"]

    def test_untrash(self, files_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        files_api.client.post.return_value = response

        result = files_api.untrash(["f1"])

        call_url = files_api.client.post.call_args[0][0]
        assert "/file/untrash/" in call_url

    def test_update_tags(self, files_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        files_api.client.post.return_value = response

        result = files_api.update_tags("f1", ["tag1", "tag2"])

        call_url = files_api.client.post.call_args[0][0]
        assert "/file/update-tags" in call_url

    def test_get_upload_url(self, files_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"url": "https://s3.example.com/upload", "file_id": "new-f1"}
        files_api.client.post.return_value = response

        result = files_api.get_upload_url("test.m4a")

        assert isinstance(result, UploadPresignedUrl)
        assert result.url == "https://s3.example.com/upload"

    def test_confirm_upload(self, files_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"status": "confirmed"}
        files_api.client.post.return_value = response

        result = files_api.confirm_upload("new-f1")

        call_url = files_api.client.post.call_args[0][0]
        assert "/file/confirm_upload" in call_url

    def test_merge_multipart(self, files_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"status": "merged"}
        files_api.client.post.return_value = response

        result = files_api.merge_multipart("new-f1")

        call_url = files_api.client.post.call_args[0][0]
        assert "/file/merge_multipart" in call_url
