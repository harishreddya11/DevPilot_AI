from pydantic import BaseModel, Field


class AssistantRequest(BaseModel):
    """
    Request schema for the AI assistant.
    """

    prompt: str = Field(
        ...,
        min_length=1,
        description="User's message to the AI assistant."
    )


class AssistantResponse(BaseModel):
    """
    Response schema for the AI assistant.
    """

    response: str
    model: str