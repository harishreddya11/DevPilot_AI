from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # ==========================================================
    # Application
    # ==========================================================
    app_name: str = "DevPilot AI"
    app_version: str = "1.0.0"
    debug: bool = True

    # ==========================================================
    # API
    # ==========================================================
    api_v1_prefix: str = "/api/v1"

    # ==========================================================
    # Security
    # ==========================================================
    secret_key: str = "change-this-in-production"

    algorithm: str = "HS256"

    access_token_expire_minutes: int = 30

    # ==========================================================
    # Database
    # ==========================================================
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "devpilot"

    # ==========================================================
    # OpenRouter
    # ==========================================================
    llm_provider: str = "openrouter"

    openrouter_api_key: str = ""

    openrouter_model: str = "deepseek/deepseek-r1-0528:free"

    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # ==========================================================
    # CORS
    # ==========================================================
    backend_cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # ==========================================================
    # File Upload
    # ==========================================================
    upload_directory: str = "uploads"

    max_upload_size_mb: int = 25

    # ==========================================================
    # Logging
    # ==========================================================
    log_level: str = "INFO"

    # ==========================================================
    # Pydantic Settings
    # ==========================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        password = quote_plus(self.postgres_password)

        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/"
            f"{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()