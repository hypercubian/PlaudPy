"""Data models for PlaudPy."""

from .ai import CustomTemplate, TaskStatus
from .auth import AccessTokenInfo, SSOProvider, TokenResponse
from .device import Device
from .file import FileDetail, FileSimple, FileTag, Recording, UploadPresignedUrl
from .membership import FreeTrialStatus, StripePrice, StripeSubscription
from .search import SavedQuery, SearchResult
from .speaker import Speaker
from .template import SummaryTemplate, TemplateCategory
from .transcript import Transcript, TranscriptEntry
from .user import (
    FeatureAccess,
    FileStats,
    TranscriptionQuota,
    UserProfile,
    UserSettings,
)

__all__ = [
    # Auth
    "TokenResponse",
    "AccessTokenInfo",
    "SSOProvider",
    # Files
    "FileSimple",
    "FileDetail",
    "FileTag",
    "Recording",
    "UploadPresignedUrl",
    # Transcript
    "TranscriptEntry",
    "Transcript",
    # AI
    "TaskStatus",
    "CustomTemplate",
    # User
    "UserProfile",
    "UserSettings",
    "FileStats",
    "TranscriptionQuota",
    "FeatureAccess",
    # Speaker
    "Speaker",
    # Search
    "SearchResult",
    "SavedQuery",
    # Template
    "SummaryTemplate",
    "TemplateCategory",
    # Membership
    "FreeTrialStatus",
    "StripePrice",
    "StripeSubscription",
    # Device
    "Device",
]
