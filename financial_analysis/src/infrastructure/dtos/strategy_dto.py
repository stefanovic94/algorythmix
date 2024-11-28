from beanie import Document
from pydantic import Field

from domain.entities import Strategy
from domain.enums import RiskTolerances


class StrategyDto(Document):
    """Represents the model/document in the database."""

    id: str = Field(
        ...,
        description="The UUID of the strategy.",
        examples=["242754ab-607c-4b14-a219-51234edf57c7"],
    )
    name: str = Field(
        ..., description="The name of the strategy.", examples=["Buy and Hold"]
    )
    risk_tolerance: RiskTolerances | None = Field(
        ...,
        description="Perceived risk tolerance of the strategy defined by the user itself. Used for labelling/categorizing strategies.",
    )

    class Settings:
        name = "Strategies"  # the MongoDB collection where documents of this model are stored
        keep_nulls = False

    def __str__(self) -> str:
        return str(self.id)

    def to_domain(self) -> Strategy:
        """
        Helper method to be used within the Repository class easily converting
        to a domain entity.

        This ensures that the DB model is only present in the infrastructure layer
        and is swiftly after being fetched from the DB converted into an entity
        that can be worked with in the domain layer.
        """
        return Strategy(
            id=self.id,
            name=self.name,
            risk_tolerance=self.risk_tolerance,
        )
