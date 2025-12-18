"""Application configuration"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://outscraper_user:temp12345@localhost:5432/outscraper"
    )
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5432"))
    DATABASE_USER: str = os.getenv("DATABASE_USER", "outscraper_user")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "temp12345")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "outscraper")

    # Connection Pool Settings
    DB_POOL_MIN_SIZE: int = int(os.getenv("DB_POOL_MIN_SIZE", "10"))
    DB_POOL_MAX_SIZE: int = int(os.getenv("DB_POOL_MAX_SIZE", "50"))
    DB_POOL_MAX_QUERIES: int = int(os.getenv("DB_POOL_MAX_QUERIES", "50000"))
    DB_POOL_MAX_INACTIVE_TIME: float = float(os.getenv("DB_POOL_MAX_INACTIVE_TIME", "300.0"))

    # API Settings
    API_TITLE: str = "Outscraper Business API"
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api/v1/outscraper"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
