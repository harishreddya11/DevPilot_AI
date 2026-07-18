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

    def generate_response(
        self,
        conversation_history: list[dict],
    ) -> str:
        """
        Generate an AI response from the conversation history.
        This is a temporary implementation until OpenRouter is integrated.
        """

        latest_prompt = conversation_history[-1]["content"]

        response = self.get_response(
            AssistantRequest(
                prompt=latest_prompt,
            )
        )

        return response.response