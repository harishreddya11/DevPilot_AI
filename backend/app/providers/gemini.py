from google import genai

from app.core.config import get_settings
from app.providers.base import BaseProvider


class GeminiProvider(BaseProvider):
    """
    Google Gemini AI Provider.
    """

    def __init__(self):
        self.settings = get_settings()

        self.client = genai.Client(
            api_key=self.settings.gemini_api_key,
        )

    

    def generate_response(
        self,
        conversation_history: list[dict],
    ) -> str:

        prompt = ""

        for message in conversation_history:
            prompt += (
                f"{message['role'].capitalize()}: "
                f"{message['content']}\n"
            )

        print("=" * 50)
        print("Provider:", self.settings.llm_provider)
        print("Model:", repr(self.settings.gemini_model))
        print("API Key Loaded:", bool(self.settings.gemini_api_key))
        print("=" * 50)

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
        )

        return response.text