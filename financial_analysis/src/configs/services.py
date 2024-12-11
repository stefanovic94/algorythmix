from functools import lru_cache

import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, ConfigDict
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError
from redis.retry import Retry

from .settings import get_settings
from libs.streams.adapters import RedisAdapter

settings = get_settings()


class Services(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cache: redis.Redis
    event_store: RedisAdapter = Field(...)
    mongodb: AsyncIOMotorClient = Field(...)


@lru_cache
def get_services() -> Services:
    redis_client = redis.Redis(
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
    )

    return Services(
        cache=redis_client,
        event_store=RedisAdapter(
            source=settings.APP_NAME,
            client=redis_client,
        ),
        mongodb=AsyncIOMotorClient(settings.NOSQL_DATABASE_CONNECTION_STRING),
    )
