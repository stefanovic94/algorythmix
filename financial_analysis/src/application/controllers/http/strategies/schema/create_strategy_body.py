from pydantic import BaseModel, Field

from domain.enums import RiskTolerances


class CreateStrategyBody(BaseModel):
    """
    Represents the request body model for the HTTP REST API
    create strategy endpoint.
    """

    name: str = Field(..., description="Name to identify the strategy by.")
    risk_tolerance: RiskTolerances | None = Field(
        None,
        description="Perceived risk tolerance of the strategy used for labeling/categorizing strategies.",
    )
