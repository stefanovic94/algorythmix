from pydantic import BaseModel, Field


class Strategy(BaseModel):
    id: str = Field(
        ...,
        description="The UUID of the strategy.",
        examples=["242754ab-607c-4b14-a219-51234edf57c7"],
    )
    name: str = Field(
        ..., description="The name of the strategy.", examples=["Buy and Hold"]
    )

    def __str__(self) -> str:
        return str(self.id)
