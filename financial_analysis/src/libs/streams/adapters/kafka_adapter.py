import asyncio
from typing import Any

from confluent_kafka import Producer, Consumer

from configs.logger import get_logger
from libs.streams.errors import (
    EventProcessingError,
    EventValidationError,
    EventNotSupported,
    EventCouldNotBeDecoded,
    EventBrokerError,
)
from libs.streams.event_handler import EventHandler
from libs.streams.models import KafkaConfig
from libs.streams.ports import EventStreamPort

logger = get_logger(__name__)


class KafkaAdapter(EventStreamPort):
    def __init__(
        self,
        source: str,
        config: KafkaConfig,
        minimum_commit_count: int = 5,
    ) -> None:
        super().__init__(source=source)
        self.__config = config
        self.__producer: Producer | None = None
        self.__consumer: Consumer | None = None
        self.__minimum_commit_count = minimum_commit_count

    async def connect(self) -> None:
        self.__producer = Producer(**self.__config.get_producer_config())
        self.__consumer = Consumer(**self.__config.get_consumer_config())

    async def close(self) -> None:
        if self.__producer is not None:
            self.__producer.flush()
        if self.__consumer is not None:
            self.__consumer.close()

    async def produce(
        self,
        topic: str,
        event_type: str,
        event_data: dict[str, Any],
        key: str | None = None,
    ) -> None:
        if self.__producer is None:
            raise EventBrokerError("Producer is not connected")

        value = self._to_cloudevents_specification(
            event_type=event_type, raw_event_data=event_data
        )
        self.__producer.produce(topic=topic, key=key, value=value)
        self.__producer.poll(0)
        self.__producer.flush()
        logger.debug("produced event - topic: %s, event: %s", topic, value)

    async def subscribe(
        self,
        event_handler: EventHandler,
        topics: list[str],
        timeout: float = 1.0,
    ) -> None:
        if self.__consumer is None:
            raise EventBrokerError("Consumer is not connected")

        self.__consumer.subscribe(topics=topics)

        logger.info("Subscribed to topics: %s", topics)

        msg_count = 0
        while True:
            msg = await asyncio.get_event_loop().run_in_executor(
                None, self.__consumer.poll, timeout
            )

            # If no message is received, continue to the next iteration
            if msg is None:
                continue

            # If an error occurs, raise an exception
            if msg.error():
                logger.critical(
                    "KafkaAdapter encountered error on message receival: %s",
                    msg.error(),
                )
                exit(1)

            # Decode the message
            try:
                decoded_msg = msg.value().decode("utf-8")
            except Exception as err:
                logger.warning("Failed to decode message: %s", err)
                continue

            # Parse the event - umatched event types are ignored
            try:
                event = event_handler.parse(event=decoded_msg)
            except (EventCouldNotBeDecoded, EventNotSupported) as err:
                logger.debug("Event could not be decoded or is not supported: %s", err)
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

            msg_count += 1
            if msg_count % self.__minimum_commit_count != 0:
                continue

            # Commit the progress regularly
            self.__consumer.commit(asynchronous=True)
