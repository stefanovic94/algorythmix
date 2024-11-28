from uuid import uuid4

from pydantic import BaseModel, Field

from domain.entities import Strategy
from domain.enums import RiskTolerances


class CreateStrategyCommand(BaseModel):
    """
    Model for specifying how to create a strategy validating data early.

    The .to_domain() method creates the unique UUID for the strategy.

    Usage
    -----
    try:
        strategy_obj = CreateStrategyCommand(name="Buy and Hold", risk_tolerance=RiskTolerances.LOW).to_domain()
    except ValidationError:
        handle_error()
    """

    name: str = Field(..., description="Name to identify the strategy by.")
    risk_tolerance: RiskTolerances | None = Field(
        None,
        description="The risk tolerance perception of the strategy. To be used for labelling strategies.",
    )

    def to_domain(self) -> Strategy:
        return Strategy(
            id=str(uuid4()),
            name=self.name,
            risk_tolerance=self.risk_tolerance,
        )
