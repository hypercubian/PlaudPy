"""PlaudPy - Python library for the Plaud.ai API."""

from .client import PlaudClient
from .config import PlaudConfig
from .exceptions import APIError, AuthenticationError, ConfigurationError, PlaudError
from .models import FileDetail, FileSimple, Recording, Transcript, TranscriptEntry

__version__ = "0.1.0"

__all__ = [
    "PlaudClient",
    "PlaudConfig",
    "PlaudError",
    "AuthenticationError",
    "APIError",
    "ConfigurationError",
    "Recording",
    "Transcript",
    "TranscriptEntry",
    "FileSimple",
    "FileDetail",
]
