from fastapi import APIRouter
from app.api.v1.projects import router as project_router

from app.api.v1 import (
    assistant,
    auth,
    chats,
    documents,
    messages,
    users,
    
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(chats.router)
api_router.include_router(messages.router)
api_router.include_router(assistant.router)
api_router.include_router(documents.router)
api_router.include_router(project_router)