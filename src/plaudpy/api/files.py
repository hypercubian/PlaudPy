"""Files API endpoints."""

from ..models import FileDetail, FileSimple
from .base import BaseAPI


class FilesAPI(BaseAPI):
    """API for file operations."""

    def list_simple(self) -> list[FileSimple]:
        """Get simple list of all files.

        Returns:
            List of FileSimple objects with basic file info.
        """
        url = f"{self.base_url}/file/simple/web"
        params = {
            "skip": 0,
            "limit": 99999,
            "sort_by": "start_time",
            "is_desc": "true",
        }
        response = self.client.get(url, headers=self.headers, params=params)
        data = self._handle_response(response)

        # API returns {"data_file_list": [...]}
        files_data = data.get("data_file_list", [])
        return [FileSimple.model_validate(f) for f in files_data]

    def get_details(self, file_ids: list[str]) -> list[FileDetail]:
        """Get detailed info for specific files.

        Args:
            file_ids: List of file IDs to fetch details for.

        Returns:
            List of FileDetail objects with transcripts and summaries.
        """
        if not file_ids:
            return []

        url = f"{self.base_url}/file/list"
        # API expects a plain list of IDs
        response = self.client.post(url, headers=self.headers, json=file_ids)
        data = self._handle_response(response)

        # API returns {"data_file_list": [...]}
        files_data = data.get("data_file_list", [])
        return [FileDetail.model_validate(f) for f in files_data]

    def trigger_transcription(self, file_id: str) -> dict:
        """Trigger transcription/summarization for a file.

        Args:
            file_id: The file ID to process.

        Returns:
            API response data.
        """
        import json
        import random

        url = f"{self.base_url}/ai/transsumm/{file_id}"
        payload = {
            "is_reload": 0,
            "summ_type": "AI-CHOICE",
            "summ_type_type": "system",
            "info": json.dumps({
                "language": "en",
                "diarization": 1,
                "llm": "openai"
            }),
            "r": random.random()
        }
        response = self.client.post(url, headers=self.headers, json=payload)
        return self._handle_response(response)
