from pydantic import BaseModel, Field

from domain.enums import RiskTolerances


class CreateStrategyBody(BaseModel):
    name: str = Field(...)
    risk_tolerance: RiskTolerances | None = Field(None)
