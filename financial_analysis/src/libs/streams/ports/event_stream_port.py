from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from libs.streams.event_handler import EventHandler


class EventStreamPort(ABC):
    def __init__(self, source: str) -> None:
        self._source = source

    @abstractmethod
    async def connect(self) -> None:
        """
        Establish a connection to the event store.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Close the connection to the event store.
        """
        pass

    def _to_cloudevents_specification(
        self, event_type: str, raw_event_data: dict[str, Any], subject: str = ""
    ) -> dict[str, Any]:
        """
        Build an event message following the CloudEvents specification.
        """
        return {
            "id": str(uuid4()),
            "source": self._source,
            "time": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "subject": subject or raw_event_data.get("_id", ""),
            "specversion": "1.0",
            "datacontenttype": "application/json",
            "data": raw_event_data,
        }

    @abstractmethod
    async def produce(
        self,
        topic: str,
        event_type: str,
        event_data: dict[str, Any],
        key: str | None = None,
    ) -> None:
        """
        Produces an event to the event broker.

        Parameters
        ----------
        topic : str
            The topic to write the event to.
        event_type : str
            The type of the event.
        event_data : dict[str, Any]
            The data of the event.
        key : str | None = None
            The key of the event subject used for partitioning.

        Returns
        -------
        None
        """
        pass

    @abstractmethod
    async def subscribe(
        self,
        event_handler: EventHandler,
        topics: list[str],
        timeout: float = 1.0,
    ) -> None:
        """
        Open subscriptions to the topics and process each incoming event based
        on the provided event handler.

        Parameters
        ----------
        event_handler : EventHandler
            The event handler which is used to process each incoming event.
        topics : list[str]
            The list of topics to subscribe to.
        timeout : float = 1.0
            The timeout between each pull from the event store.

        Returns
        -------
        None
        """
        pass
