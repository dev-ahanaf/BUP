"""Configuration settings for GridWise Energy Optimization Service."""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env."""

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # LLM Configuration
    # Supported providers: "openai", "anthropic", "openrouter", "gemini", "rule_based", "auto"
    LLM_PROVIDER: str = "auto"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_API_KEY: Optional[str] = None
    LLM_BASE_URL: Optional[str] = None
    LLM_TEMPERATURE: float = 0.0
    LLM_TIMEOUT_SECONDS: float = 15.0
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # Optimizer Configuration
    OPTIMIZER_SOLVER: str = "CBC"  # "CBC", "SCIP", "GLOP"
    OPTIMIZER_TIME_LIMIT_SECONDS: float = 5.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
