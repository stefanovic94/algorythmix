from uuid import uuid4

from pydantic import BaseModel, Field

from domain.entities import Strategy
from domain.enums import RiskTolerances


class CreateStrategyCommand(BaseModel):
    name: str = Field(...)
    risk_tolerance: RiskTolerances | None = Field(...)

    def to_domain(self) -> Strategy:
        return Strategy(
            id=str(uuid4()),
            name=self.name,
            risk_tolerance=self.risk_tolerance,
        )
