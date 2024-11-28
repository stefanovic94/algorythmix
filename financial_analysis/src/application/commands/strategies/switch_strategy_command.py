from pydantic import BaseModel, Field


class SwitchStrategyCommand(BaseModel):
    current_strategy: str = Field(
        ..., description="ID of the strategy currently applied."
    )
    new_strategy: str = Field(
        ..., description="ID of the strategy to switch into using as applied strategy."
    )
