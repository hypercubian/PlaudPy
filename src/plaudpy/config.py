"""Configuration management for PlaudPy."""

from pydantic_settings import BaseSettings


class PlaudConfig(BaseSettings):
    """Configuration loaded from environment variables."""

    username: str | None = None
    password: str | None = None
    base_url: str = "https://api.plaud.ai"
    client_id: str = "web"

    model_config = {
        "env_prefix": "PLAUD_",
        "env_file": ".env",
        "extra": "ignore",
    }
