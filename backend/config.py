from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "OmniAgent API"
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    llm_provider: str = "stub"
    llm_model: str = "llama3.2:3b"

    redis_url: str = "redis://redis:6379/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
