"""AI API endpoints."""

import json
import random

from ..models.ai import CustomTemplate, TaskStatus
from .base import BaseAPI


class AIAPI(BaseAPI):
    """API for AI transcription and summarization operations."""

    def trigger_transcription(
        self,
        file_id: str,
        language: str = "en",
        is_reload: int = 0,
        summ_type: str = "AI-CHOICE",
        summ_type_type: str = "system",
        diarization: int = 1,
        llm: str = "openai",
    ) -> dict:
        """Trigger transcription/summarization for a file.

        Args:
            file_id: The file ID to process.
            language: Transcription language.
            is_reload: Whether to reload existing transcription.
            summ_type: Summary template type.
            summ_type_type: Whether template is 'system' or 'custom'.
            diarization: Enable speaker diarization (1=yes, 0=no).
            llm: LLM provider to use.
        """
        payload = {
            "is_reload": is_reload,
            "summ_type": summ_type,
            "summ_type_type": summ_type_type,
            "info": json.dumps({
                "language": language,
                "diarization": diarization,
                "llm": llm,
            }),
            "r": random.random(),
        }
        return self._post(f"/ai/transsumm/{file_id}", json=payload)

    def update_transsumm(self, transsumm_id: str, **kwargs) -> dict:
        """Update a transcription/summarization record.

        Args:
            transsumm_id: The transsumm ID to update.
            **kwargs: Fields to update.
        """
        return self._patch(f"/transsumm/{transsumm_id}", json=kwargs)

    def get_task_status(self) -> dict:
        """Get status of AI processing tasks."""
        return self._get("/ai/task-status")

    def get_file_task_status(self) -> dict:
        """Get file-level AI task status."""
        return self._get("/ai/file-task-status")

    def get_recently_used_language(self) -> dict:
        """Get the most recently used transcription language."""
        return self._get("/ai/recently_used_language")

    def list_custom_templates(self) -> list[CustomTemplate]:
        """List user's custom summary templates."""
        data = self._get("/ai/customtemplates")
        items = data if isinstance(data, list) else data.get("data", [])
        return [CustomTemplate.model_validate(item) for item in items]

    def create_custom_template(self, name: str, prompt: str) -> CustomTemplate:
        """Create a new custom summary template.

        Args:
            name: Template name.
            prompt: Template prompt text.
        """
        data = self._post("/ai/customtemplates", json={"name": name, "prompt": prompt})
        return CustomTemplate.model_validate(data)

    def update_custom_template(self, template_id: str, **kwargs) -> CustomTemplate:
        """Update a custom summary template.

        Args:
            template_id: Template ID to update.
            **kwargs: Fields to update (name, prompt).
        """
        data = self._patch(f"/ai/customtemplates/{template_id}", json=kwargs)
        return CustomTemplate.model_validate(data)

    def delete_custom_template(self, template_id: str) -> dict:
        """Delete a custom summary template.

        Args:
            template_id: Template ID to delete.
        """
        return self._delete(f"/ai/customtemplates/{template_id}")

    def label(self, **kwargs) -> dict:
        """Apply AI labels to content.

        Args:
            **kwargs: Label parameters.
        """
        return self._post("/ai/label", json=kwargs)

    def update_note_info(self, **kwargs) -> dict:
        """Update note information.

        Args:
            **kwargs: Note info parameters.
        """
        return self._post("/ai/update_note_info", json=kwargs)

    def delete_note_info(self, **kwargs) -> dict:
        """Delete note information.

        Args:
            **kwargs: Note identification parameters.
        """
        return self._post("/ai/del_note_info", json=kwargs)

    def update_source_info(self, **kwargs) -> dict:
        """Update source information.

        Args:
            **kwargs: Source info parameters.
        """
        return self._post("/ai/update_source_info", json=kwargs)

    def extract_speaker_embedding(self, **kwargs) -> dict:
        """Extract speaker embedding from a clip.

        Args:
            **kwargs: Clip identification parameters (e.g. file_id, start_time, end_time).
        """
        return self._post("/ai/speaker-embedding/extract-by-clip", json=kwargs)
