from pydantic import BaseModel, Field


class DeleteStrategyCommand(BaseModel):
    id: str = Field(..., description="ID of the strategy to delete.")
