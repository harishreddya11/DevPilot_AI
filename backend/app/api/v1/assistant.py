from fastapi import APIRouter

from app.schemas.assistant import AssistantRequest, AssistantResponse
from app.services.assistant_service import AssistantService

router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"],
)

assistant_service = AssistantService()


@router.post(
    "/",
    response_model=AssistantResponse,
)
def assistant(
    request: AssistantRequest,
) -> AssistantResponse:
    """
    Send a prompt to the AI assistant.
    """
    return assistant_service.get_response(request)