from pydantic import BaseModel, Field, model_validator, ValidationError
from typing_extensions import Self

from configs.settings import get_settings
from libs.streams import Event

settings = get_settings()


class EventData(BaseModel):
    id: str = Field(..., description="ID of the strategy.")
    name: str = Field(..., description="Name of the strategy.")


class StrategyCreated(Event):
    """
    Represents a strategy created event.

    Based on the pydantic BaseModel type for easier validation and testing without
    having to manage a schema registry.
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
        print(f"producing {self.__class__} event")

    async def process(self) -> None:
        raise NotImplementedError(
            "Not implemented as it is currently not expected to receive this kind of event within this service."
        )
