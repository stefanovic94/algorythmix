from beanie import Document
from pydantic import Field

from domain.entities import Strategy


class StrategyDto(Document):
    id: str = Field(
        ...,
        description="The UUID of the strategy.",
        examples=["242754ab-607c-4b14-a219-51234edf57c7"],
    )
    name: str = Field(
        ..., description="The name of the strategy.", examples=["Buy and Hold"]
    )

    class Settings:
        name = "Strategies"
        keep_nulls = False

    def __str__(self) -> str:
        return str(self.id)

    def to_domain(self) -> Strategy:
        return Strategy(
            id=self.id,
            name=self.name,
        )
