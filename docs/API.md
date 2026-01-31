# Plaud.ai API Documentation

Base URL: `https://api.plaud.ai`

## Authentication

### POST `/auth/access-token`
Authenticate and obtain an access token.

**Request:** `multipart/form-data`
| Field | Type | Description |
|-------|------|-------------|
| `username` | string | Email address |
| `password` | string | Password |
| `client_id` | string | Client identifier (`web`, `ios`, `android`) |

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 25920000
}
```

**Auth Header for subsequent requests:**
```
Authorization: Bearer {access_token}
```

---

## Files

### GET `/file/simple/web`
Get a paginated list of files with basic info.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `skip` | int | Offset for pagination (default: 0) |
| `limit` | int | Number of records (default: 20, max: 99999) |
| `sort_by` | string | Sort field (`start_time`) |
| `is_desc` | bool | Descending order (`true`/`false`) |

**Response:**
```json
{
  "status": 0,
  "msg": "success",
  "request_id": "",
  "data_file_total": 25,
  "data_file_list": [
    {
      "id": "abc123...",
      "filename": "Meeting Recording",
      "filesize": 3303200,
      "filetype": null,
      "fullname": "abc123.opus",
      "file_md5": "4c8a6d5f...",
      "duration": 825000,
      "start_time": 1769531126000,
      "end_time": 1769531951000,
      "edit_time": 1769620084,
      "edit_from": "ios",
      "is_trash": false,
      "scene": 1,
      "serial_number": "888316991542872883",
      "is_trans": true,
      "is_summary": true,
      "wait_pull": 0,
      "filetag_id_list": [],
      "keywords": []
    }
  ]
}
```

**File Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique file identifier |
| `filename` | string | User-visible name |
| `filesize` | int | File size in bytes |
| `fullname` | string | Original filename with extension |
| `duration` | int | Duration in milliseconds |
| `start_time` | int | Recording start (Unix ms) |
| `end_time` | int | Recording end (Unix ms) |
| `is_trans` | bool | Has transcription |
| `is_summary` | bool | Has AI summary |
| `scene` | int | Recording scene type (1=meeting, etc.) |
| `serial_number` | string | Device serial number |
| `filetag_id_list` | array | List of tag IDs |

---

### POST `/file/list`
Get detailed file info including transcripts and summaries.

**Request Body:** Array of file IDs
```json
["abc123", "def456"]
```

**Response:**
```json
{
  "status": 0,
  "msg": "success",
  "data_file_list": [
    {
      "id": "abc123",
      "filename": "Meeting Recording",
      "trans_result": [...],
      "ai_content": "## Summary...",
      "outline_result": [...],
      "notes_list": [...],
      "file_language": "en",
      "download_link_map": {...}
    }
  ]
}
```

**Additional Detail Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `trans_result` | array | Transcript entries |
| `ai_content` | string | AI-generated summary (markdown) |
| `outline_result` | array | Meeting outline/agenda |
| `notes_list` | array | User notes |
| `file_language` | string | Detected language |
| `download_link_map` | object | Download URLs |
| `ori_fullname` | string | Original audio filename |
| `ori_location` | string | Storage path |
| `channel` | int | Audio channels |
| `session_id` | int | Session identifier |

---

### GET `/file/detail/{file_id}`
Get file metadata (lighter than `/file/list`).

**Response:**
```json
{
  "status": 0,
  "data": {
    "file_id": "abc123",
    "file_name": "Meeting",
    "file_version": 1769620084,
    "duration": 825000,
    "start_time": 1769531126000,
    "scene": 1,
    "serial_number": "888316991542872883",
    "session_id": 1769531126,
    "filetag_id_list": [],
    "content_list": [],
    "embeddings": {},
    "download_path_mapping": {},
    "extra_data": {}
  }
}
```

---

### GET `/file/download/{file_id}`
Download the audio file.

**Response:** Binary audio data (`application/octet-stream`)

---

### POST `/file/upload`
Initialize a file upload.

**Response:**
```json
{
  "status": 0,
  "msg": "success",
  "data_file": {...},
  "temp_file_id": "..."
}
```

---

## AI / Transcription

### POST `/ai/transsumm/{file_id}`
Trigger transcription and summarization for a file.

**Request Body:**
```json
{
  "is_reload": 0,
  "summ_type": "AI-CHOICE",
  "summ_type_type": "system",
  "info": "{\"language\":\"en\",\"diarization\":1,\"llm\":\"openai\"}",
  "r": 0.123456
}
```

**Parameters:**
| Field | Type | Description |
|-------|------|-------------|
| `is_reload` | int | Force re-process (0=no, 1=yes) |
| `summ_type` | string | Summary template type |
| `summ_type_type` | string | Template category (`system`/`custom`) |
| `info` | string | JSON with language, diarization, LLM settings |
| `r` | float | Random cache buster |

**Info JSON Options:**
| Field | Values | Description |
|-------|--------|-------------|
| `language` | `en`, `zh`, `es`, etc. | Target language |
| `diarization` | 0, 1 | Speaker identification |
| `llm` | `openai` | LLM provider |

---

### GET `/ai/status`
Get current AI processing status.

**Response:**
```json
{
  "status": 0,
  "data_processing": [],
  "data_processing_chatllm": [],
  "data_processing_transsumm": {
    "files_trans": [],
    "files_summ": [],
    "files_outline": []
  },
  "data_transsumm": {
    "files_trans": [],
    "files_summ": []
  },
  "data_processing_edit": [],
  "data_processing_sum_new_note": [],
  "data_complete_sum_new_note": []
}
```

---

## Devices

### GET `/device/list`
Get list of registered Plaud devices.

**Response:**
```json
{
  "status": 0,
  "msg": "success",
  "data_devices": [
    {
      "sn": "888316991542872883",
      "name": "Plaud Note",
      "model": "888",
      "version_number": 95
    }
  ]
}
```

---

## Data Structures

### Transcript Entry
```json
{
  "start_time": 3360,
  "end_time": 33910,
  "content": "Hello, this is the transcript text...",
  "speaker": "Speaker 1",
  "original_speaker": "Speaker 1"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `start_time` | int | Start time in milliseconds |
| `end_time` | int | End time in milliseconds |
| `content` | string | Transcript text |
| `speaker` | string | Identified speaker label |
| `original_speaker` | string | Original speaker (before renaming) |

### AI Summary Format
The `ai_content` field contains markdown-formatted summary:

```markdown
## Meeting Information
> Date: 2026-01-28 15:46:55
> Location: [Insert Location]
> Participants: [Speaker 1] [Speaker 2] [Adam]

## Meeting Notes

### Topic 1
- Point 1
- Point 2

### Action Items
- [ ] Task 1 - Assigned to Speaker 1
- [ ] Task 2 - Assigned to Speaker 2
```

---

## Error Responses

All endpoints return:
```json
{
  "status": 1,
  "msg": "error message",
  "request_id": "..."
}
```

| Status Code | Meaning |
|-------------|---------|
| 0 | Success |
| 1 | Generic error |
| 401 | Unauthorized |
| 404 | Not found |
| 405 | Method not allowed |

---

## Discovered but Unverified Endpoints

These endpoints exist based on the web app but weren't fully tested:

- `POST /file/update` - Update file metadata
- `POST /file/batch/delete` - Batch delete files
- `POST /file/batch/restore` - Restore from trash
- `GET /file/tags` - File tags/labels (405 - needs POST?)
- `POST /share/create` - Share a file
- `POST /note/add` - Add notes to a file

---

## Web App Routes

The web application (`web.plaud.ai`) has these routes:
- `/login` - Authentication
- `/` - Dashboard/file list
- `/file/{id}` - File detail view
- `/downloads` - Downloads page
- `/sharing` - Shared files
- `/privacy` - Privacy policy
- `/agreement` - Terms of service
