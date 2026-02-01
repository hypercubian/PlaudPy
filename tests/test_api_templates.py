"""Unit tests for Templates API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.templates import TemplatesAPI
from plaudpy.config import PlaudConfig
from plaudpy.models.template import SummaryTemplate, TemplateCategory


@pytest.fixture
def templates_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = TemplatesAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestTemplatesAPI:

    def test_list_chatllm_templates(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "t1", "name": "Meeting Notes", "is_system": True}]}
        templates_api.client.get.return_value = response

        result = templates_api.list_chatllm_templates()

        assert len(result) == 1
        assert isinstance(result[0], SummaryTemplate)
        assert result[0].name == "Meeting Notes"

    def test_get_recommended_templates(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "t1", "name": "Action Items"}]}
        templates_api.client.get.return_value = response

        result = templates_api.get_recommended_templates()
        assert len(result) == 1

    def test_get_template_categories(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "c1", "name": "Business"}]}
        templates_api.client.get.return_value = response

        result = templates_api.get_template_categories()

        assert len(result) == 1
        assert isinstance(result[0], TemplateCategory)
        assert result[0].name == "Business"

    def test_search_community_templates(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "ct1", "name": "Interview Summary"}]}
        templates_api.client.post.return_value = response

        result = templates_api.search_community_templates("interview")

        assert len(result) == 1
        call_url = templates_api.client.post.call_args[0][0]
        assert "/community-template/search" in call_url

    def test_create_community_template(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "ct1", "name": "My Template", "prompt": "Summarize"}
        templates_api.client.post.return_value = response

        result = templates_api.create_community_template("My Template", "Summarize")

        assert isinstance(result, SummaryTemplate)
        assert result.name == "My Template"

    def test_edit_community_template(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "ct1", "name": "Updated"}
        templates_api.client.patch.return_value = response

        result = templates_api.edit_community_template("ct1", name="Updated")
        assert isinstance(result, SummaryTemplate)

    def test_delete_community_template(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        templates_api.client.delete.return_value = response

        templates_api.delete_community_template("ct1")
        call_url = templates_api.client.delete.call_args[0][0]
        assert "/community-template/ct1" in call_url

    def test_favorite_template(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        templates_api.client.post.return_value = response

        templates_api.favorite_template("ct1")
        call_url = templates_api.client.post.call_args[0][0]
        assert "/community-template/ct1/favorite" in call_url

    def test_unfavorite_template(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        templates_api.client.post.return_value = response

        templates_api.unfavorite_template("ct1")
        call_url = templates_api.client.post.call_args[0][0]
        assert "/community-template/ct1/unfavorite" in call_url

    def test_list_favorite_templates(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "ct1", "name": "Fav"}]}
        templates_api.client.get.return_value = response

        result = templates_api.list_favorite_templates()
        assert len(result) == 1

    def test_get_community_home(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"featured": [], "popular": []}
        templates_api.client.get.return_value = response

        result = templates_api.get_community_home()
        assert "featured" in result

    def test_list_my_templates(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": []}
        templates_api.client.get.return_value = response

        result = templates_api.list_my_templates()
        assert result == []

    def test_list_recently_used(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "t1", "name": "Recent"}]}
        templates_api.client.get.return_value = response

        result = templates_api.list_recently_used()
        assert len(result) == 1

    def test_get_daily_recommendations(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": []}
        templates_api.client.get.return_value = response

        result = templates_api.get_daily_recommendations()
        assert result == []

    def test_get_weekly_recommendations(self, templates_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": []}
        templates_api.client.get.return_value = response

        result = templates_api.get_weekly_recommendations()
        assert result == []
