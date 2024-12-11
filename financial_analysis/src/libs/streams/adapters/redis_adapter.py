import asyncio
from typing import Any

import redis.asyncio as redis
from redis import ResponseError

from configs.logger import get_logger
from libs.streams.errors import (
    EventProcessingError,
    EventValidationError,
    EventNotSupported,
    EventCouldNotBeDecoded,
)
from libs.streams.event_handler import EventHandler
from libs.streams.ports import EventStreamPort
import random
import string

logger = get_logger(__name__)


class RedisAdapter(EventStreamPort):
    def __init__(
        self,
        source: str,
        client: redis.Redis,
        minimum_commit_count: int = 1,
        batch_size: int = 1,
    ) -> None:
        super().__init__(source=source)
        self.__client = client
        self.__consumer_name = f"{self._source}-" + "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        self.__minimum_commit_count = minimum_commit_count
        self.__batch_size = batch_size
        self.__subscribed_topics = []

    async def __create_group(self, topic: str, name: str) -> None:
        try:
            await self.__client.xgroup_create(
                name=topic, groupname=name, id="$", mkstream=True
            )
        except ResponseError as err:
            logger.warning(
                "topic: %s, group name: %s, tried creating consumer group in Redis. It may already exist. Error: %s",
                topic,
                name,
                err,
            )

    async def connect(self) -> None:
        pass

    async def close(self) -> None:
        # clean up consumer from all subscribed topics
        for topic in self.__subscribed_topics:
            await self.__client.xgroup_delconsumer(
                topic, self._source, self.__consumer_name
            )

        await self.__client.aclose(close_connection_pool=True)

    async def produce(
        self,
        topic: str,
        event_type: str,
        event_data: dict[str, Any],
        key: str | None = None,
    ) -> None:
        value = self._to_cloudevents_specification(
            event_type=event_type, raw_event_data=event_data
        )

        await self.__client.xadd(topic, value)

        logger.debug("produced event - topic: %s, event: %s", topic, value)

    async def subscribe(
        self,
        event_handler: EventHandler,
        topics: list[str],
        timeout: float = 1.0,
    ) -> None:
        for topic in topics:
            await self.__create_group(topic=topic, name=self._source)
            await self.__client.xgroup_createconsumer(
                topic, self._source, self.__consumer_name
            )
            self.__subscribed_topics.append(topic)

        received_msgs = []
        try:
            while True:
                for stream, messages in await self.__client.xreadgroup(
                    groupname=self._source,
                    consumername=self.__consumer_name,
                    streams={topic: ">" for topic in topics},
                    count=self.__batch_size,
                ):
                    for message_id, message in messages:
                        # Parse the event - umatched event types are ignored
                        try:
                            event = event_handler.parse(event=message)
                        except (EventCouldNotBeDecoded, EventNotSupported) as err:
                            logger.debug(
                                "Event could not be decoded or is not supported: %s",
                                err,
                            )
                            continue  # Skip the message if it's not a valid event

                        # Process the event - can fail with validation error if event data is invalid
                        try:
                            await event_handler.process(event=event)
                        except EventValidationError as err:
                            logger.debug("Event validation error: %s", err)
                            continue
                        except EventProcessingError as e:
                            logger.critical("Error while processing event: %s", e)
                            exit(1)

                        received_msgs.append(message_id)
                        if len(received_msgs) % self.__minimum_commit_count != 0:
                            continue

                        # Acknowledge the received messages
                        for received_msg in received_msgs:
                            await self.__client.xack(stream, self._source, received_msg)
                        received_msgs.clear()

                await asyncio.sleep(timeout)
        except KeyboardInterrupt:
            logger.info("Shutting down Redis consumer")
