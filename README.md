# PlaudPy

Python library for interfacing with the Plaud.ai API.

## Installation

```bash
pip install plaudpy
```

Or with Poetry:

```bash
poetry add plaudpy
```

## Usage

### Environment Variables

Set your Plaud credentials as environment variables:

```bash
export PLAUD_USERNAME=your_email@example.com
export PLAUD_PASSWORD=your_password
```

Or create a `.env` file:

```
PLAUD_USERNAME=your_email@example.com
PLAUD_PASSWORD=your_password
```

### Basic Usage

```python
from plaudpy import PlaudClient

# Uses PLAUD_USERNAME/PLAUD_PASSWORD from environment
client = PlaudClient()

# Or provide credentials explicitly
client = PlaudClient(username="email@example.com", password="secret")

# Get all recordings
for recording in client.get_recordings():
    print(f"Title: {recording.title}")
    print(f"Duration: {recording.duration}s")
    print(f"Summary: {recording.summary}")
    print(f"Transcript: {recording.transcript.to_text()}")
    print("---")

# Get a single recording
recording = client.get_recording("file-id-here")

# Export to markdown
markdown = recording.to_markdown()
print(markdown)
```

### Context Manager

```python
with PlaudClient() as client:
    recordings = client.get_recordings()
    for r in recordings:
        print(r.title)
```

## API Reference

### PlaudClient

- `get_recordings()` - Get all recordings with transcripts and summaries
- `get_recording(file_id)` - Get a single recording by ID
- `trigger_transcription(file_id)` - Trigger transcription/summarization for a file

### Recording

- `id` - File ID
- `title` - Recording title
- `duration` - Duration in seconds
- `created_at` - Creation timestamp
- `transcript` - Transcript object
- `summary` - AI-generated summary
- `to_markdown()` - Export to markdown format

### Transcript

- `entries` - List of TranscriptEntry objects
- `to_text(include_speakers=True)` - Convert to plain text
- `to_markdown(include_timestamps=False)` - Convert to markdown

## Development

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest
```

## License

MIT
