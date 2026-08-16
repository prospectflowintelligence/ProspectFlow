"""Application configuration.

All configuration is sourced from environment variables so the same image
can run in local Docker, CI, and any future cloud environment without code
changes. See /.env.example at the repo root for the full list of variables.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- App ---
    PROJECT_NAME: str = "ProspectFlow API"
    ENVIRONMENT: str = "local"  # local | ci | staging | production
    API_V1_PREFIX: str = "/api/v1"

    # --- Security ---
    SECRET_KEY: str = "CHANGE_ME_IN_ENV"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h — MVP only, will shrink + add refresh tokens later
    JWT_ALGORITHM: str = "HS256"

    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg://prospectflow:prospectflow@localhost:5432/prospectflow"

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    @property
    def is_local(self) -> bool:
        return self.ENVIRONMENT == "local"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
