from pydantic import BaseModel, Field

from domain.enums import RiskTolerances


class Strategy(BaseModel):
    """
    The Strategy entity represents a strategy that can be applied to the
    financial analysis processes.
    """

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

    def __str__(self) -> str:
        return str(self.id)
