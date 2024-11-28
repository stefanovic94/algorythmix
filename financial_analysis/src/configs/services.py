import socket
from functools import lru_cache

import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, ConfigDict
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError
from redis.retry import Retry

from .settings import get_settings
from libs.streams.adapters import KafkaAdapter
from libs.streams.models import KafkaConfig

settings = get_settings()


class Services(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cache: redis.Redis
    event_store: KafkaAdapter = Field(...)
    mongodb: AsyncIOMotorClient = Field(...)


@lru_cache
def get_services() -> Services:
    return Services(
        cache=redis.Redis(
            connection_pool=redis.ConnectionPool.from_url(
                settings.CACHE_URL,
                max_connections=settings.CACHE_MAX_CONNECTIONS,
                retry=Retry(ExponentialBackoff(), 3),
                retry_on_timeout=True,
                retry_on_error=[ConnectionError, TimeoutError, BusyLoadingError],
                decode_responses=True,
                socket_timeout=settings.CACHE_SOCKET_TIMEOUT,
                socket_connect_timeout=settings.CACHE_SOCKET_CONNECT_TIMEOUT,
            )
        ),
        event_store=KafkaAdapter(
            source=settings.APP_NAME,
            config=KafkaConfig(
                host=settings.KAFKA_URL,
                enable_cert_verification=False,
                username=settings.KAFKA_USERNAME,
                password=settings.KAFKA_PASSWORD,
                client_id=settings.APP_NAME + "-" + socket.gethostname(),
                queue_buffering_max_messages=10_000_000,
                compression_type="gzip",
                linger=1_000,
                batch_size=32_000,
                group_id=settings.APP_NAME,
                session_timeout=350_000,
                max_poll_interval=350_000,
                auto_offset_reset="earliest",
                fetch_min_bytes=10_000,
            ),
            minimum_commit_count=settings.KAFKA_MIN_COMMIT_COUNT,
        ),
        mongodb=AsyncIOMotorClient(settings.NOSQL_DATABASE_CONNECTION_STRING),
    )
