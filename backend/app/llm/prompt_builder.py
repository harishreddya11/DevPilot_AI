from app.schemas.assistant import AssistantRequest


class PromptBuilder:
    """
    Builds prompts before sending them
    to the LLM provider.
    """

    @staticmethod
    def build(
        request: AssistantRequest,
    ) -> str:

        return f"""
You are DevPilot AI.

You are an expert software engineer.

Answer the following user request.

User:
{request.prompt}
""".strip()