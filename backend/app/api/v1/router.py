from fastapi import APIRouter
from app.api.v1.router import api_router
from app.api.v1 import (
    assistant,
    auth,
    chats,
    messages,
    users,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(chats.router)
api_router.include_router(messages.router)   # <-- Must be present
api_router.include_router(assistant.router)
