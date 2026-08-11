"""Application settings, loaded from the environment."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Every field is overridable via a PYLON_ env var."""

    model_config = SettingsConfigDict(
        env_prefix="PYLON_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+psycopg://pylon:pylon@localhost:5433/pylon"
    log_level: str = "INFO"
    echo_sql: bool = False


def get_settings() -> Settings:
    """Return settings.

    Not cached deliberately: tests override the environment and expect it to take
    effect. If this ever shows up in a profile, cache it then, not before.
    """
    return Settings()
