from pydantic import BaseModel, Field, model_validator, ValidationError
from typing_extensions import Self

from configs.logger import get_logger
from configs.settings import get_settings
from libs.streams import Event

logger = get_logger(__name__)
settings = get_settings()


class EventData(BaseModel):
    """Represents the format of the `data` key in the event payload."""

    id: str = Field(..., description="ID of the strategy.")
    name: str = Field(..., description="Name of the strategy.")


class StrategyCreated(Event):
    """
    Represents a `strategy created` event. This event is being produced by the `CreateStategyCommand`
    in the application layer.

    This class contains the logic of what the event should look like and where
    it should be produced (e.g. Kafka, internal pub/sub, etc.).

    Based on the pydantic BaseModel type for easier validation without
    having to manage a schema registry, and easier testing without having to
    spin up infrastructure dependencies.
    """

    subject: str = Field("")
    source: str = Field(settings.APP_NAME)
    spec_version: str = Field("1.0")
    type: str = Field("FinancialAnalysis.Strategy.v1")
    data_content_type: str = Field("application/json")
    data: EventData = Field(...)

    @model_validator(mode="after")
    def populate_subject(self) -> Self:
        """
        Overwrites the `subject` key with the ID of the strategy object.

        Raises
        ------
        ValidationError
            If the `id` field is not present in the `data` object.
        """

        if getattr(self.data, "id", None) is None:
            raise ValidationError("The `id` field of the `data` object is required.")

        self.subject = self.data.id
        return self

    async def produce(self) -> None:
        logger.info("producing %s event", self.__class__)

    async def process(self) -> None:
        raise NotImplementedError(
            "Not implemented as it is currently not expected to receive this kind of event within this service."
        )
