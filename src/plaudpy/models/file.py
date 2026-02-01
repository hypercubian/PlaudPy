"""File and recording models."""

from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from .transcript import Transcript, TranscriptEntry


class FileSimple(BaseModel):
    """Simple file info from /file/simple/web endpoint."""

    id: str
    filename: str = ""
    duration: int = 0
    start_time: int = Field(default=0)

    model_config = {"populate_by_name": True}

    @property
    def title(self) -> str:
        return self.filename

    @property
    def created_at(self) -> datetime | None:
        if self.start_time:
            return datetime.fromtimestamp(self.start_time / 1000.0, tz=timezone.utc)
        return None


class FileDetail(BaseModel):
    """Detailed file info from /file/list endpoint."""

    id: str
    filename: str = ""
    duration: int = 0
    start_time: int = Field(default=0)
    transcript_data: list[dict] | None = Field(default=None, alias="trans_result")
    summary: str | None = Field(default=None, alias="ai_content")
    language: str | None = Field(default=None)

    model_config = {"populate_by_name": True}

    @property
    def title(self) -> str:
        return self.filename

    @property
    def created_at(self) -> datetime | None:
        if self.start_time:
            return datetime.fromtimestamp(self.start_time / 1000.0, tz=timezone.utc)
        return None

    def get_transcript(self) -> Transcript:
        """Parse transcript data into a Transcript object."""
        if not self.transcript_data:
            return Transcript(language=self.language)

        entries = []
        for item in self.transcript_data:
            entry = TranscriptEntry(
                speaker=item.get("speaker") or "",
                text=item.get("content") or "",
                start_time=(item.get("start_time") or 0) / 1000.0,  # Convert ms to seconds
                end_time=(item.get("end_time") or 0) / 1000.0,
            )
            entries.append(entry)

        return Transcript(entries=entries, language=self.language)


class Recording(BaseModel):
    """A recording with its transcript and summary."""

    id: str
    title: str
    duration: int = 0
    created_at: datetime | None = None
    transcript: Transcript = Field(default_factory=Transcript)
    summary: str | None = None
    language: str | None = None

    @classmethod
    def from_file_detail(cls, detail: FileDetail) -> "Recording":
        """Create a Recording from FileDetail."""
        return cls(
            id=detail.id,
            title=detail.title,
            duration=detail.duration,
            created_at=detail.created_at,
            transcript=detail.get_transcript(),
            summary=detail.summary,
            language=detail.language,
        )

    def to_markdown(self, include_timestamps: bool = False) -> str:
        """Export recording to markdown format.

        Args:
            include_timestamps: Whether to include timestamps in transcript.

        Returns:
            Markdown representation of the recording.
        """
        lines = [f"# {self.title}", ""]

        if self.created_at:
            lines.append(f"**Date:** {self.created_at.strftime('%Y-%m-%d %H:%M')}")

        if self.duration:
            minutes = self.duration // 60
            seconds = self.duration % 60
            lines.append(f"**Duration:** {minutes}:{seconds:02d}")

        lines.append("")

        if self.summary:
            lines.extend(["## Summary", "", self.summary, ""])

        if self.transcript.entries:
            lines.extend([
                "## Transcript",
                "",
                self.transcript.to_markdown(include_timestamps=include_timestamps),
            ])

        return "\n".join(lines)


class FileTag(BaseModel):
    """A file tag."""

    model_config = {"extra": "allow"}

    id: str | None = None
    name: str | None = None
    color: str | None = None


class UploadPresignedUrl(BaseModel):
    """Pre-signed URL for file upload."""

    model_config = {"extra": "allow"}

    url: str | None = None
    file_id: str | None = None
    fields: dict | None = None
