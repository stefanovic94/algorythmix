import json
from typing import Any, Type

from pydantic import ValidationError

from libs.streams.errors import (
    EventNotSupported,
    EventCouldNotBeDecoded,
    EventValidationError,
    EventProcessingError,
)
from libs.streams.models import Event


class EventHandler:
    """
    Handling incoming events by parsing and processing them.

    Methods
    -------
    parse(event: dict[str, Any] | str) -> Event
        Parses an event message into an Event object.
    process(event: Event) -> None
        Processes an Event object.
    """

    def __init__(self, supported_events: list[Type[Event]]) -> None:
        self.supported_events = supported_events

    def __decode_event(self, event: dict[str, Any] | str | None) -> dict[str, Any]:
        if event is None:
            raise EventCouldNotBeDecoded("Event is null")

        if isinstance(event, str):
            decoded_msg = json.loads(event)
        else:
            decoded_msg = event
        return decoded_msg

    def __parse_event(self, decoded_msg: dict[str, Any]) -> Event:
        parsed_event = None
        if not self.supported_events:
            raise EventNotSupported("No supported events are set")
        for event_type in self.supported_events:
            try:
                parsed_event = event_type(**decoded_msg)
            except ValidationError:
                continue
            break
        if parsed_event is None:
            raise EventNotSupported(f"Event {decoded_msg} is not supported")
        return parsed_event

    def parse(self, event: dict[str, Any] | str) -> Event:
        """
        Parses an event message into an Event object.

        Parameters
        ----------
        event : dict[str, Any] | str
            The event message to parse.

        Returns
        -------
        Event
            The parsed Event object.

        Raises
        ------
        EventNotSupported
            If the event is not supported.
        EventCouldNotBeDecoded
            If the event is null.
        """
        decoded_msg = self.__decode_event(event=event)
        return self.__parse_event(decoded_msg=decoded_msg)

    async def process(self, event: Event) -> None:
        """
        Processes an Event object.

        Parameters
        ----------
        event : Event
            The Event object to process.

        Raises
        ------
        EventValidationError
            If the event is invalid.
        """
        try:
            await event.process()
        except ValidationError as e:
            raise EventValidationError(
                f"Event type {event.type} with ID {event.id} is invalid: {e}"
            )
        except Exception as e:
            raise EventProcessingError(
                f"Error while processing event {event.type} with ID {event.id}: {e}"
            )
