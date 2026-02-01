"""Devices API endpoints."""

from ..models.device import Device
from .base import BaseAPI


class DevicesAPI(BaseAPI):
    """API for device operations."""

    def list_devices(self) -> list[Device]:
        """List all registered Plaud devices."""
        data = self._get("/device/list")
        items = data if isinstance(data, list) else data.get("data", [])
        return [Device.model_validate(item) for item in items]
