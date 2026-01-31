"""Pytest configuration and fixtures."""

import os

import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "functional: marks tests as functional (require credentials)"
    )


@pytest.fixture
def sample_transcript_data():
    """Sample transcript data as returned by the API."""
    return [
        {
            "speaker": "Speaker 1",
            "content": "Hello, how are you?",
            "start_time": 0,
            "end_time": 2000,
        },
        {
            "speaker": "Speaker 2",
            "content": "I'm doing well, thanks!",
            "start_time": 2500,
            "end_time": 4000,
        },
        {
            "speaker": "Speaker 1",
            "content": "Great to hear.",
            "start_time": 4500,
            "end_time": 5500,
        },
    ]


@pytest.fixture
def sample_file_simple_data():
    """Sample FileSimple data as returned by the API."""
    return {
        "id": "abc123",
        "filename": "Test Recording",
        "duration": 300,
        "start_time": 1700000000000,
    }


@pytest.fixture
def sample_file_detail_data(sample_transcript_data):
    """Sample FileDetail data as returned by the API."""
    return {
        "id": "abc123",
        "filename": "Test Recording",
        "duration": 300,
        "start_time": 1700000000000,
        "trans_result": sample_transcript_data,
        "ai_content": "This is a summary of the meeting.",
        "language": "en",
    }


@pytest.fixture
def sample_files_response(sample_file_simple_data):
    """Sample response from /file/simple/web endpoint."""
    return {
        "data_file_list": [
            sample_file_simple_data,
            {
                "id": "def456",
                "filename": "Another Recording",
                "duration": 600,
                "start_time": 1700100000000,
            },
        ]
    }


@pytest.fixture
def sample_file_details_response(sample_file_detail_data):
    """Sample response from /file/list endpoint."""
    return {
        "data_file_list": [sample_file_detail_data]
    }


@pytest.fixture(scope="module")
def plaud_credentials():
    """Get Plaud credentials from environment."""
    username = os.environ.get("PLAUD_USERNAME")
    password = os.environ.get("PLAUD_PASSWORD")

    if not username or not password:
        pytest.skip("PLAUD_USERNAME and PLAUD_PASSWORD must be set")

    return {"username": username, "password": password}
