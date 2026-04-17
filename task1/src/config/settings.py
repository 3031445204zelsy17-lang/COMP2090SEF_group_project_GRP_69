"""Application Configuration"""

import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings class."""

    # DeepSeek API
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v1/chat/completions"
    deepseek_model: str = "deepseek-chat"

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    # Application settings
    app_secret_key: str = "dev-secret-key"
    app_env: str = "development"
    app_name: str = "Automatic Email Reply System"
    app_version: str = "1.0.0"

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env == "production"


@lru_cache()
def get_settings() -> Settings:
    """Get the cached settings singleton."""
    return Settings()
