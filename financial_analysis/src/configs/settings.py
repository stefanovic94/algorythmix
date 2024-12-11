from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: Literal["dev", "staging", "production"] = Field("dev")
    APP_NAME: str = Field("financial_analysis", frozen=True)
    LOGGING_LEVEL: Literal["debug", "info", "warning", "error", "critical"] = Field(
        "info"
    )
    NOSQL_DATABASE_CONNECTION_STRING: str = Field(
        "mongodb://localhost:27017/",
        description="Connection string to access the NoSQL database.",
        examples=["mongodb+srv://app:somepassword@someatlasclusterhost.mongodb.net/"],
    )
    CACHE_URL: str = Field(
        "redis://default:somepassword@localhost:6379",
        description="Connection URL for the cache instance.",
        examples=["rediss://app:somepassword@somerediscloudhost.redis-cloud.com:port"],
    )
    CACHE_MAX_CONNECTIONS: int = Field(
        30, description="Maximum number of connections to the cache."
    )
    CACHE_SOCKET_TIMEOUT: int = Field(
        600, description="Timeout for socket connections."
    )
    CACHE_SOCKET_CONNECT_TIMEOUT: int = Field(
        600, description="Timeout for connection establishment."
    )
    KAFKA_URL: str = Field(
        "localhost:9093", description="URL of the kafka instance/cluster."
    )
    KAFKA_USERNAME: str = Field(
        "", description="Username for accessing the kafka instance/cluster."
    )
    KAFKA_PASSWORD: str = Field(
        "", description="Password for accessing the kafka instance/cluster."
    )
    KAFKA_MIN_COMMIT_COUNT: int = Field(
        5,
        description="Specifies the interval when the progress on the event stream is being committed to the kafka instance/cluster measured in number of messages received.",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
