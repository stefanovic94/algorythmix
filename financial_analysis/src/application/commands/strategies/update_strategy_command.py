from pydantic import BaseModel, Field

from domain.entities import Strategy
from domain.enums import RiskTolerances


class UpdateStrategyCommand(BaseModel):
    """
    Model defining how to update a strategy.
    """

    strategy: Strategy = Field(..., description="The strategy to update.")
    name: str | None = Field(None, description="Change the name of the strategy.")
    risk_tolerance: RiskTolerances | None = Field(
        None, description="Change the risk tolerance of the strategy."
    )
