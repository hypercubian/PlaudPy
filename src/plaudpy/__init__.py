"""PlaudPy - Python library for the Plaud.ai API."""

from .client import PlaudClient
from .config import PlaudConfig
from .exceptions import APIError, AuthenticationError, ConfigurationError, PlaudError
from .models import (
    AccessTokenInfo,
    CustomTemplate,
    Device,
    FeatureAccess,
    FileDetail,
    FileSimple,
    FileStats,
    FileTag,
    FreeTrialStatus,
    Recording,
    SavedQuery,
    SearchResult,
    Speaker,
    SSOProvider,
    StripePrice,
    StripeSubscription,
    SummaryTemplate,
    TaskStatus,
    TemplateCategory,
    Transcript,
    TranscriptEntry,
    TranscriptionQuota,
    UploadPresignedUrl,
    UserProfile,
    UserSettings,
)

__version__ = "0.2.0"

__all__ = [
    # Client
    "PlaudClient",
    "PlaudConfig",
    # Exceptions
    "PlaudError",
    "AuthenticationError",
    "APIError",
    "ConfigurationError",
    # Core models
    "Recording",
    "Transcript",
    "TranscriptEntry",
    "FileSimple",
    "FileDetail",
    "FileTag",
    "UploadPresignedUrl",
    # Auth models
    "AccessTokenInfo",
    "SSOProvider",
    # AI models
    "TaskStatus",
    "CustomTemplate",
    # User models
    "UserProfile",
    "UserSettings",
    "FileStats",
    "TranscriptionQuota",
    "FeatureAccess",
    # Speaker models
    "Speaker",
    # Search models
    "SearchResult",
    "SavedQuery",
    # Template models
    "SummaryTemplate",
    "TemplateCategory",
    # Membership models
    "FreeTrialStatus",
    "StripePrice",
    "StripeSubscription",
    # Device models
    "Device",
]
