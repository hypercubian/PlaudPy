"""Device-related models."""

from pydantic import BaseModel


class Device(BaseModel):
    """A Plaud device."""

    model_config = {"extra": "allow"}

    id: str | None = None
    name: str | None = None
    model: str | None = None
    firmware_version: str | None = None
    serial_number: str | None = None
