"""Unit tests for Search API."""

from unittest.mock import MagicMock

import httpx
import pytest

from plaudpy.api.search import SearchAPI
from plaudpy.config import PlaudConfig
from plaudpy.models.search import SavedQuery, SearchResult


@pytest.fixture
def search_api():
    config = PlaudConfig(username="test", password="test")
    client = MagicMock(spec=httpx.Client)
    api = SearchAPI(config, client)
    api.set_access_token("test-token")
    return api


class TestSearchAPI:

    def test_search(self, search_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {
            "results": [
                {"id": "r1", "title": "Meeting Notes", "snippet": "...discussed budget...", "file_id": "f1"}
            ]
        }
        search_api.client.post.return_value = response

        result = search_api.search("budget")

        assert len(result) == 1
        assert isinstance(result[0], SearchResult)
        assert result[0].title == "Meeting Notes"
        call_url = search_api.client.post.call_args[0][0]
        assert "/gsearch/v1/search" in call_url

    def test_list_saved_queries(self, search_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"data": [{"id": "sq1", "query": "meeting"}]}
        search_api.client.get.return_value = response

        result = search_api.list_saved_queries()

        assert len(result) == 1
        assert isinstance(result[0], SavedQuery)
        assert result[0].query == "meeting"

    def test_create_saved_query(self, search_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {"id": "sq2", "query": "project update"}
        search_api.client.post.return_value = response

        result = search_api.create_saved_query("project update")

        assert isinstance(result, SavedQuery)
        assert result.query == "project update"

    def test_delete_saved_query(self, search_api):
        response = MagicMock(status_code=200)
        response.json.return_value = {}
        search_api.client.delete.return_value = response

        result = search_api.delete_saved_query("sq1")

        call_url = search_api.client.delete.call_args[0][0]
        assert "/gsearch/v1/saved-queries/sq1" in call_url
