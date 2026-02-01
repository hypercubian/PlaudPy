"""Unit tests for AI API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.ai import AIAPI
from plaudpy.config import PlaudConfig
from plaudpy.models.ai import CustomTemplate


@pytest.fixture
def ai_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = AIAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestAIAPI:

    def test_trigger_transcription(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"status": "processing"}
        ai_api.client.post.return_value = response

        result = ai_api.trigger_transcription("file-123")

        ai_api.client.post.assert_called_once()
        call_url = ai_api.client.post.call_args[0][0]
        assert "/ai/transsumm/file-123" in call_url
        assert result == {"status": "processing"}

    def test_update_transsumm(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "ts-1"}
        ai_api.client.patch.return_value = response

        result = ai_api.update_transsumm("ts-1", title="New Title")

        call_url = ai_api.client.patch.call_args[0][0]
        assert "/transsumm/ts-1" in call_url

    def test_get_task_status(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"tasks": []}
        ai_api.client.get.return_value = response

        result = ai_api.get_task_status()

        call_url = ai_api.client.get.call_args[0][0]
        assert "/ai/task-status" in call_url

    def test_get_file_task_status(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"tasks": []}
        ai_api.client.get.return_value = response

        result = ai_api.get_file_task_status()

        call_url = ai_api.client.get.call_args[0][0]
        assert "/ai/file-task-status" in call_url

    def test_get_recently_used_language(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"language": "en"}
        ai_api.client.get.return_value = response

        result = ai_api.get_recently_used_language()
        assert result == {"language": "en"}

    def test_list_custom_templates(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "t1", "name": "My Template", "prompt": "Summarize"}]}
        ai_api.client.get.return_value = response

        result = ai_api.list_custom_templates()

        assert len(result) == 1
        assert isinstance(result[0], CustomTemplate)
        assert result[0].name == "My Template"

    def test_create_custom_template(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "t1", "name": "Test", "prompt": "Do stuff"}
        ai_api.client.post.return_value = response

        result = ai_api.create_custom_template("Test", "Do stuff")

        assert isinstance(result, CustomTemplate)
        assert result.name == "Test"

    def test_update_custom_template(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "t1", "name": "Updated"}
        ai_api.client.patch.return_value = response

        result = ai_api.update_custom_template("t1", name="Updated")
        assert isinstance(result, CustomTemplate)

    def test_delete_custom_template(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        ai_api.client.delete.return_value = response

        result = ai_api.delete_custom_template("t1")

        call_url = ai_api.client.delete.call_args[0][0]
        assert "/ai/customtemplates/t1" in call_url

    def test_label(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"status": "ok"}
        ai_api.client.post.return_value = response

        result = ai_api.label(file_id="f1", label="important")

        call_url = ai_api.client.post.call_args[0][0]
        assert "/ai/label" in call_url

    def test_update_note_info(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        ai_api.client.post.return_value = response

        result = ai_api.update_note_info(file_id="f1", note="test")

        call_url = ai_api.client.post.call_args[0][0]
        assert "/ai/update_note_info" in call_url

    def test_delete_note_info(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        ai_api.client.post.return_value = response

        result = ai_api.delete_note_info(file_id="f1")

        call_url = ai_api.client.post.call_args[0][0]
        assert "/ai/del_note_info" in call_url

    def test_update_source_info(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        ai_api.client.post.return_value = response

        result = ai_api.update_source_info(file_id="f1")

        call_url = ai_api.client.post.call_args[0][0]
        assert "/ai/update_source_info" in call_url

    def test_extract_speaker_embedding(self, ai_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"embedding": [0.1, 0.2]}
        ai_api.client.post.return_value = response

        result = ai_api.extract_speaker_embedding(file_id="f1", start_time=0, end_time=5)

        call_url = ai_api.client.post.call_args[0][0]
        assert "/ai/speaker-embedding/extract-by-clip" in call_url
