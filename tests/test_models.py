"""Unit tests for PlaudPy models."""

from datetime import datetime, timezone

import pytest

from plaudpy.models import (
    FileDetail,
    FileSimple,
    Recording,
    Transcript,
    TranscriptEntry,
)


class TestTranscriptEntry:
    """Tests for TranscriptEntry model."""

    def test_create_entry(self):
        entry = TranscriptEntry(
            speaker="Speaker 1",
            text="Hello world",
            start_time=1.5,
            end_time=3.0,
        )
        assert entry.speaker == "Speaker 1"
        assert entry.text == "Hello world"
        assert entry.start_time == 1.5
        assert entry.end_time == 3.0

    def test_default_values(self):
        entry = TranscriptEntry()
        assert entry.speaker == ""
        assert entry.text == ""
        assert entry.start_time == 0.0
        assert entry.end_time == 0.0


class TestTranscript:
    """Tests for Transcript model."""

    def test_to_text_with_speakers(self):
        entries = [
            TranscriptEntry(speaker="Alice", text="Hello"),
            TranscriptEntry(speaker="Bob", text="Hi there"),
        ]
        transcript = Transcript(entries=entries)

        text = transcript.to_text(include_speakers=True)
        assert text == "Alice: Hello\nBob: Hi there"

    def test_to_text_without_speakers(self):
        entries = [
            TranscriptEntry(speaker="Alice", text="Hello"),
            TranscriptEntry(speaker="Bob", text="Hi there"),
        ]
        transcript = Transcript(entries=entries)

        text = transcript.to_text(include_speakers=False)
        assert text == "Hello\nHi there"

    def test_to_markdown_groups_by_speaker(self):
        entries = [
            TranscriptEntry(speaker="Alice", text="Hello"),
            TranscriptEntry(speaker="Alice", text="How are you?"),
            TranscriptEntry(speaker="Bob", text="Good, thanks!"),
        ]
        transcript = Transcript(entries=entries)

        md = transcript.to_markdown()
        assert "**Alice**" in md
        assert "**Bob**" in md
        assert md.count("**Alice**") == 1  # Should group consecutive entries

    def test_to_markdown_with_timestamps(self):
        entries = [
            TranscriptEntry(speaker="Alice", text="Hello", start_time=1.5),
        ]
        transcript = Transcript(entries=entries)

        md = transcript.to_markdown(include_timestamps=True)
        assert "[1.5s]" in md

    def test_empty_transcript(self):
        transcript = Transcript()
        assert transcript.entries == []
        assert transcript.to_text() == ""
        assert transcript.to_markdown() == ""


class TestFileSimple:
    """Tests for FileSimple model."""

    def test_parse_from_api_data(self, sample_file_simple_data):
        file = FileSimple.model_validate(sample_file_simple_data)

        assert file.id == "abc123"
        assert file.filename == "Test Recording"
        assert file.title == "Test Recording"
        assert file.duration == 300

    def test_created_at_property(self, sample_file_simple_data):
        file = FileSimple.model_validate(sample_file_simple_data)

        assert file.created_at is not None
        assert isinstance(file.created_at, datetime)
        assert file.created_at.tzinfo == timezone.utc

    def test_created_at_none_when_no_start_time(self):
        file = FileSimple(id="test", filename="Test")
        assert file.created_at is None


class TestFileDetail:
    """Tests for FileDetail model."""

    def test_parse_from_api_data(self, sample_file_detail_data):
        file = FileDetail.model_validate(sample_file_detail_data)

        assert file.id == "abc123"
        assert file.title == "Test Recording"
        assert file.summary == "This is a summary of the meeting."
        assert file.language == "en"

    def test_get_transcript(self, sample_file_detail_data):
        file = FileDetail.model_validate(sample_file_detail_data)
        transcript = file.get_transcript()

        assert isinstance(transcript, Transcript)
        assert len(transcript.entries) == 3
        assert transcript.entries[0].speaker == "Speaker 1"
        assert transcript.entries[0].text == "Hello, how are you?"
        # Times should be converted from ms to seconds
        assert transcript.entries[0].start_time == 0.0
        assert transcript.entries[0].end_time == 2.0

    def test_get_transcript_empty(self):
        file = FileDetail(id="test", filename="Test")
        transcript = file.get_transcript()

        assert isinstance(transcript, Transcript)
        assert len(transcript.entries) == 0


class TestRecording:
    """Tests for Recording model."""

    def test_from_file_detail(self, sample_file_detail_data):
        detail = FileDetail.model_validate(sample_file_detail_data)
        recording = Recording.from_file_detail(detail)

        assert recording.id == "abc123"
        assert recording.title == "Test Recording"
        assert recording.summary == "This is a summary of the meeting."
        assert len(recording.transcript.entries) == 3

    def test_to_markdown(self, sample_file_detail_data):
        detail = FileDetail.model_validate(sample_file_detail_data)
        recording = Recording.from_file_detail(detail)

        md = recording.to_markdown()

        assert "# Test Recording" in md
        assert "## Summary" in md
        assert "This is a summary of the meeting." in md
        assert "## Transcript" in md
        assert "**Speaker 1**" in md

    def test_to_markdown_with_duration(self):
        recording = Recording(
            id="test",
            title="Test",
            duration=125,  # 2:05
        )

        md = recording.to_markdown()
        assert "**Duration:** 2:05" in md

    def test_to_markdown_with_timestamps(self, sample_file_detail_data):
        detail = FileDetail.model_validate(sample_file_detail_data)
        recording = Recording.from_file_detail(detail)

        md = recording.to_markdown(include_timestamps=True)
        assert "[0.0s]" in md
