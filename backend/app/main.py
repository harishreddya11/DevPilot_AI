from fastapi import FastAPI
from app.core.exception_handlers import register_exception_handlers
from app.api.v1.assistant import router as assistant_router
from app.api.v1.health import router as health_router
from app.core.config import get_settings
from app.api.v1.auth import router as auth_router
from app.core.logging import setup_logging
from app.core.middleware import log_requests
from app.api.v1.users import router as users_router
from app.api.v1.chats import router as chats_router
from app.api.v1.messages import router as messages_router
from app.api.v1.documents import router as documents_router
from app.api.v1.endpoints.test import router as test_router

# Load application settings
settings = get_settings()

# Create the FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="An AI-powered developer workspace.",
)

register_exception_handlers(app)
app.middleware("http")(log_requests)

# Register API routers
app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    assistant_router,
    prefix="/api/v1",
)

app.include_router(test_router)

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    users_router, 
    prefix="/api/v1"
)

app.include_router(
    chats_router,
    prefix="/api/v1",
)

app.include_router(
    messages_router,
    prefix="/api/v1",
)

app.include_router(
    documents_router,
    prefix="/api/v1",
)
@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint.
    """
    return {
        "message": f"Welcome to {settings.app_name} 🚀",
        "version": settings.app_version,
    }