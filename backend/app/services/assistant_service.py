from app.providers.provider_factory import ProviderFactory


class AssistantService:
    """
    Handles AI response generation using the configured provider.
    """

    def __init__(self):
        self.provider = ProviderFactory.get_provider()

    def generate_response(
        self,
        conversation_history: list[dict],
    ) -> str:
        """
        Generate an AI response using the configured provider.
        """
        return self.provider.generate_response(conversation_history)