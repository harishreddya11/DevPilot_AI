import httpx

from app.core.config import get_settings
from app.providers.base_provider import BaseProvider


class OpenRouterProvider(BaseProvider):
    """
    OpenRouter AI Provider.
    """

    def __init__(self):
        self.settings = get_settings()

    def generate_response(
        self,
        conversation_history: list[dict],
    ) -> str:

        headers = {
            "Authorization": f"Bearer {self.settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "DevPilot AI",
        }

        payload = {
            "model": self.settings.openrouter_model,
            "messages": conversation_history,
        }

        try:
            response = httpx.post(
                f"{self.settings.openrouter_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as exc:
            error = exc.response.json()
            raise Exception(
                error["error"]["message"]
            )

        except Exception as exc:
            raise Exception(
                f"Failed to generate AI response: {str(exc)}"
            )