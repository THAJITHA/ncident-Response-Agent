from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "incident-response-agent"
    app_env: str = "development"
    database_url: str = "sqlite:///./incident_agent.db"
    api_base_url: str = "http://localhost:8000"
    llm_provider: Literal["groq", "openai", "mock"] = "groq"
    groq_api_key: str = ""
    openai_api_key: str = ""
    hindsight_api_key: str = ""
    hindsight_api_url: str = "https://api.hindsight.vectorize.io"
    hindsight_bank_id: str = "incident-response"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
