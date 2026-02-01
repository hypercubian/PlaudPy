"""API layer for PlaudPy."""

from .ai import AIAPI
from .auth import AuthAPI
from .base import BaseAPI
from .config_api import ConfigAPI
from .devices import DevicesAPI
from .files import FilesAPI
from .membership import MembershipAPI
from .misc import MiscAPI
from .search import SearchAPI
from .speakers import SpeakersAPI
from .tags import TagsAPI
from .templates import TemplatesAPI
from .users import UsersAPI

__all__ = [
    "BaseAPI",
    "AIAPI",
    "AuthAPI",
    "ConfigAPI",
    "DevicesAPI",
    "FilesAPI",
    "MembershipAPI",
    "MiscAPI",
    "SearchAPI",
    "SpeakersAPI",
    "TagsAPI",
    "TemplatesAPI",
    "UsersAPI",
]
