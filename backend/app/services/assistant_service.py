from app.schemas.assistant import AssistantRequest, AssistantResponse


class AssistantService:
    """
    Handles the business logic for the AI assistant.
    """

    def get_response(
        self,
        request: AssistantRequest,
    ) -> AssistantResponse:
        """
        Return a dummy AI response.
        """

        return AssistantResponse(
            response=f"You said: {request.prompt}",
            model="dummy-provider",
        )