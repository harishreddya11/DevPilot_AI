from fastapi import FastAPI
from app.core.exception_handlers import register_exception_handlers
from app.api.v1.assistant import router as assistant_router
from app.api.v1.health import router as health_router
from app.core.config import get_settings
from app.api.v1.auth import router as auth_router
from app.core.logging import setup_logging
from app.core.middleware import log_requests
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

app.include_router(
    auth_router,
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