"""
Core configuration module.
Loads settings from environment variables / .env file using pydantic-settings.
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── App ───────────────────────────────────────────────────────────────
    APP_NAME: str = Field(default="SaaS API", description="Application name")
    DEBUG: bool = Field(default=False, description="Debug mode")

    # ── Database ──────────────────────────────────────────────────────────
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/saas_db",
        description="Async PostgreSQL connection string",
    )

    # ── JWT / Auth ────────────────────────────────────────────────────────
    JWT_SECRET: str = Field(
        default="super-secret-change-me-in-production",
        description="Secret key used to sign JWT tokens",
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT signing algorithm")
    JWT_EXPIRE_MINUTES: int = Field(
        default=60, description="Access-token lifetime in minutes"
    )

    # ── Server ────────────────────────────────────────────────────────────
    API_PORT: int = Field(default=8000, description="Backend API port")
    API_HOST: str = Field(default="0.0.0.0", description="Backend API host")
    FRONTEND_PORT: int = Field(default=4200, description="Frontend dev-server port")

    # ── CORS ──────────────────────────────────────────────────────────────
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:4200", "http://localhost:3000", "https://saas-api-1-h0y5.onrender.com"],
        description="Allowed CORS origins",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()


# Singleton instance – import this wherever settings are needed.
settings = Settings()
