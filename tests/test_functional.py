"""Functional tests against the real Plaud.ai API.

These tests require valid PLAUD_USERNAME and PLAUD_PASSWORD environment variables.
Run with: pytest tests/test_functional.py -v
"""

import os

import pytest

from plaudpy import PlaudClient, Recording


# Skip all tests in this module if credentials are not set
pytestmark = pytest.mark.functional


@pytest.fixture(scope="module")
def client(plaud_credentials):
    """Create a PlaudClient with real credentials."""
    c = PlaudClient(**plaud_credentials)
    yield c
    c.close()


class TestAuthentication:
    """Test authentication against real API."""

    def test_successful_login(self, plaud_credentials):
        """Should successfully authenticate with valid credentials."""
        client = PlaudClient(**plaud_credentials)
        # If we get here without exception, auth succeeded
        assert client._files_api._access_token is not None
        client.close()


class TestGetRecordings:
    """Test fetching recordings from real API."""

    def test_get_recordings_returns_list(self, client):
        """Should return a list of recordings."""
        recordings = client.get_recordings()

        assert isinstance(recordings, list)
        print(f"\nFound {len(recordings)} recordings")

    def test_recordings_have_required_fields(self, client):
        """Each recording should have id and title."""
        recordings = client.get_recordings()

        if not recordings:
            pytest.skip("No recordings available in account")

        for recording in recordings:
            assert recording.id, "Recording should have an ID"
            assert recording.title, "Recording should have a title"
            print(f"  - {recording.title} ({recording.id})")

    def test_recordings_have_transcripts(self, client):
        """Recordings with transcripts should have parsed entries."""
        recordings = client.get_recordings()

        if not recordings:
            pytest.skip("No recordings available in account")

        recordings_with_transcripts = [
            r for r in recordings if r.transcript.entries
        ]

        if not recordings_with_transcripts:
            pytest.skip("No recordings with transcripts available")

        recording = recordings_with_transcripts[0]
        print(f"\nRecording: {recording.title}")
        print(f"Transcript entries: {len(recording.transcript.entries)}")
        print(f"First entry: {recording.transcript.entries[0].text[:100]}...")

        assert len(recording.transcript.entries) > 0

    def test_recordings_have_summaries(self, client):
        """Recordings with summaries should have summary text."""
        recordings = client.get_recordings()

        if not recordings:
            pytest.skip("No recordings available in account")

        recordings_with_summaries = [r for r in recordings if r.summary]

        if not recordings_with_summaries:
            pytest.skip("No recordings with summaries available")

        recording = recordings_with_summaries[0]
        print(f"\nRecording: {recording.title}")
        print(f"Summary preview: {recording.summary[:200]}...")

        assert recording.summary


class TestGetSingleRecording:
    """Test fetching a single recording."""

    def test_get_recording_by_id(self, client):
        """Should fetch a single recording by ID."""
        # First get all recordings to find a valid ID
        recordings = client.get_recordings()

        if not recordings:
            pytest.skip("No recordings available in account")

        recording_id = recordings[0].id
        recording = client.get_recording(recording_id)

        assert recording is not None
        assert isinstance(recording, Recording)
        assert recording.id == recording_id


class TestMarkdownExport:
    """Test markdown export functionality."""

    def test_to_markdown_output(self, client):
        """Should generate valid markdown output."""
        recordings = client.get_recordings()

        if not recordings:
            pytest.skip("No recordings available in account")

        # Find a recording with both transcript and summary
        recording = next(
            (r for r in recordings if r.transcript.entries and r.summary),
            recordings[0]
        )

        md = recording.to_markdown()

        print(f"\n--- Markdown Output ---\n{md[:1000]}...")

        assert f"# {recording.title}" in md
        if recording.summary:
            assert "## Summary" in md
        if recording.transcript.entries:
            assert "## Transcript" in md
