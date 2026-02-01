"""Unit tests for new PlaudPy models."""

import pytest

from plaudpy.models.ai import CustomTemplate, TaskStatus
from plaudpy.models.auth import AccessTokenInfo, SSOProvider
from plaudpy.models.device import Device
from plaudpy.models.file import FileTag, UploadPresignedUrl
from plaudpy.models.membership import FreeTrialStatus, StripePrice, StripeSubscription
from plaudpy.models.search import SavedQuery, SearchResult
from plaudpy.models.speaker import Speaker
from plaudpy.models.template import SummaryTemplate, TemplateCategory
from plaudpy.models.user import (
    FeatureAccess,
    FileStats,
    TranscriptionQuota,
    UserProfile,
    UserSettings,
)


class TestAuthModels:

    def test_access_token_info(self):
        info = AccessTokenInfo(id="tok1", client_id="web", created_at="2024-01-01")
        assert info.id == "tok1"
        assert info.client_id == "web"

    def test_access_token_info_extra_fields(self):
        info = AccessTokenInfo.model_validate({"id": "tok1", "unknown_field": "value"})
        assert info.id == "tok1"

    def test_sso_provider(self):
        provider = SSOProvider(provider="google", name="Google", bound=True)
        assert provider.provider == "google"
        assert provider.bound is True


class TestAIModels:

    def test_task_status(self):
        status = TaskStatus(file_id="f1", status="processing", progress=0.5)
        assert status.file_id == "f1"
        assert status.progress == 0.5

    def test_custom_template(self):
        template = CustomTemplate(id="t1", name="My Template", prompt="Summarize this")
        assert template.name == "My Template"
        assert template.prompt == "Summarize this"

    def test_custom_template_extra_fields(self):
        template = CustomTemplate.model_validate({"id": "t1", "custom_field": 42})
        assert template.id == "t1"


class TestUserModels:

    def test_user_profile(self):
        profile = UserProfile(id="u1", email="test@example.com", nickname="Test")
        assert profile.email == "test@example.com"

    def test_user_settings_extra_fields(self):
        settings = UserSettings.model_validate({"theme": "dark", "language": "en"})
        # Extra fields should be allowed

    def test_file_stats(self):
        stats = FileStats(total_files=42, total_duration=3600)
        assert stats.total_files == 42
        assert stats.total_duration == 3600

    def test_transcription_quota(self):
        quota = TranscriptionQuota(total=300, used=100, remaining=200)
        assert quota.total == 300
        assert quota.remaining == 200

    def test_feature_access(self):
        access = FeatureAccess.model_validate({"premium": True, "beta": False})
        # Extra fields allowed


class TestFileModels:

    def test_file_tag(self):
        tag = FileTag(id="t1", name="Work", color="#ff0000")
        assert tag.name == "Work"
        assert tag.color == "#ff0000"

    def test_upload_presigned_url(self):
        url = UploadPresignedUrl(url="https://s3.example.com/upload", file_id="f1")
        assert url.url == "https://s3.example.com/upload"
        assert url.file_id == "f1"


class TestSpeakerModels:

    def test_speaker(self):
        speaker = Speaker(id="s1", name="Alice")
        assert speaker.name == "Alice"

    def test_speaker_extra_fields(self):
        speaker = Speaker.model_validate({"id": "s1", "name": "Bob", "embedding": [0.1, 0.2]})
        assert speaker.name == "Bob"


class TestSearchModels:

    def test_search_result(self):
        result = SearchResult(id="r1", title="Meeting", snippet="budget discussion", file_id="f1")
        assert result.title == "Meeting"
        assert result.file_id == "f1"

    def test_saved_query(self):
        query = SavedQuery(id="sq1", query="meeting notes")
        assert query.query == "meeting notes"


class TestTemplateModels:

    def test_summary_template(self):
        template = SummaryTemplate(id="t1", name="Notes", prompt="Take notes", is_system=True)
        assert template.name == "Notes"
        assert template.is_system is True

    def test_template_category(self):
        category = TemplateCategory(id="c1", name="Business")
        assert category.name == "Business"


class TestMembershipModels:

    def test_free_trial_status(self):
        status = FreeTrialStatus(eligible=True, active=False, days_remaining=7)
        assert status.eligible is True
        assert status.days_remaining == 7

    def test_stripe_price(self):
        price = StripePrice(id="price_1", product="pro", currency="usd", unit_amount=999, interval="month")
        assert price.unit_amount == 999
        assert price.interval == "month"

    def test_stripe_subscription(self):
        sub = StripeSubscription(id="sub_1", status="active", plan="pro")
        assert sub.status == "active"


class TestDeviceModels:

    def test_device(self):
        device = Device(id="d1", name="My Plaud Note", model="PN-1", firmware_version="2.1.0")
        assert device.name == "My Plaud Note"
        assert device.model == "PN-1"

    def test_device_extra_fields(self):
        device = Device.model_validate({"id": "d1", "battery_level": 85})
        assert device.id == "d1"
