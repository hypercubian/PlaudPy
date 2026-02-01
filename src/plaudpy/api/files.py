"""Files API endpoints."""

from ..models.file import FileDetail, FileSimple, UploadPresignedUrl
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

    def get_detail(self, file_id: str) -> FileDetail:
        """Get detailed metadata for a single file.

        Args:
            file_id: The file ID.
        """
        data = self._get(f"/file/detail/{file_id}")
        return FileDetail.model_validate(data)

    def download(self, file_id: str) -> bytes:
        """Download a file's audio content.

        Args:
            file_id: The file ID to download.

        Returns:
            Raw file bytes.
        """
        url = f"{self.base_url}/file/download/{file_id}"
        response = self.client.get(url, headers=self.headers)
        return self._handle_binary_response(response)

    def update(self, file_id: str, **kwargs) -> dict:
        """Update file metadata.

        Args:
            file_id: The file ID to update.
            **kwargs: Fields to update (e.g. filename).
        """
        return self._patch(f"/file/{file_id}", json=kwargs)

    def trash(self, file_ids: list[str]) -> dict:
        """Move files to trash.

        Args:
            file_ids: List of file IDs to trash.
        """
        return self._post("/file/trash/", json=file_ids)

    def untrash(self, file_ids: list[str]) -> dict:
        """Restore files from trash.

        Args:
            file_ids: List of file IDs to restore.
        """
        return self._post("/file/untrash/", json=file_ids)

    def update_tags(self, file_ids: str | list[str], tag_id: str) -> dict:
        """Apply a tag to one or more files.

        Args:
            file_ids: A single file ID or list of file IDs.
            tag_id: The tag ID to apply.
        """
        if isinstance(file_ids, str):
            file_ids = [file_ids]
        return self._post("/file/update-tags", json={"file_id_list": file_ids, "filetag_id": tag_id})

    def get_upload_url(self, filename: str, **kwargs) -> UploadPresignedUrl:
        """Get a pre-signed URL for file upload.

        Args:
            filename: Name of the file to upload.
            **kwargs: Additional upload parameters.
        """
        payload = {"filename": filename, **kwargs}
        data = self._post("/file/get_upload_presigned_url", json=payload)
        return UploadPresignedUrl.model_validate(data)

    def confirm_upload(self, file_id: str, **kwargs) -> dict:
        """Confirm a completed file upload.

        Args:
            file_id: The file ID from the upload URL response.
            **kwargs: Additional confirmation parameters.
        """
        payload = {"file_id": file_id, **kwargs}
        return self._post("/file/confirm_upload", json=payload)

    def merge_multipart(self, file_id: str, **kwargs) -> dict:
        """Merge multipart upload parts.

        Args:
            file_id: The file ID.
            **kwargs: Additional merge parameters.
        """
        payload = {"file_id": file_id, **kwargs}
        return self._post("/file/merge_multipart", json=payload)
