from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: Literal["dev", "staging", "production"] = Field("dev")
    APP_NAME: str = Field("trading", frozen=True)
    LOGGING_LEVEL: Literal["debug", "info", "warning", "error", "critical"] = Field(
        "info"
    )
    CACHE_URL: str = Field(..., description="Connection URL for the cache instance.")
    CACHE_MAX_CONNECTIONS: int = Field(
        30, description="Maximum number of connections to the cache."
    )
    CACHE_SOCKET_TIMEOUT: int = Field(
        600, description="Timeout for socket connections."
    )
    CACHE_SOCKET_CONNECT_TIMEOUT: int = Field(
        600, description="Timeout for connection establishment."
    )
    NOSQL_DATABASE_CONNECTION_STRING: str = Field(
        ..., description="Connection string to access the NoSQL database."
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
