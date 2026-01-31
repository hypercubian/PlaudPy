"""Transcript models."""

from pydantic import BaseModel, Field


class TranscriptEntry(BaseModel):
    """A single entry in a transcript."""

    speaker: str = ""
    text: str = ""
    start_time: float = 0.0
    end_time: float = 0.0


class Transcript(BaseModel):
    """A complete transcript with multiple entries."""

    entries: list[TranscriptEntry] = Field(default_factory=list)
    language: str | None = None

    def to_text(self, include_speakers: bool = True) -> str:
        """Convert transcript to plain text.

        Args:
            include_speakers: Whether to include speaker labels.

        Returns:
            Plain text representation of the transcript.
        """
        lines = []
        for entry in self.entries:
            if include_speakers and entry.speaker:
                lines.append(f"{entry.speaker}: {entry.text}")
            else:
                lines.append(entry.text)
        return "\n".join(lines)

    def to_markdown(self, include_timestamps: bool = False) -> str:
        """Convert transcript to markdown format.

        Args:
            include_timestamps: Whether to include timestamps.

        Returns:
            Markdown representation of the transcript.
        """
        lines = []
        current_speaker = None

        for entry in self.entries:
            if entry.speaker != current_speaker:
                current_speaker = entry.speaker
                speaker_label = f"**{entry.speaker}**" if entry.speaker else "**Speaker**"
                lines.append(f"\n{speaker_label}\n")

            if include_timestamps:
                timestamp = f"[{entry.start_time:.1f}s] "
                lines.append(f"{timestamp}{entry.text}")
            else:
                lines.append(entry.text)

        return "\n".join(lines)
