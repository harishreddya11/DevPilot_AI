from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AuthenticationError)
    async def authentication_exception_handler(
        request: Request,
        exc: AuthenticationError,
    ):
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AuthorizationError)
    async def authorization_exception_handler(
        request: Request,
        exc: AuthorizationError,
    ):
        return JSONResponse(
            status_code=403,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotFoundError)
    async def not_found_exception_handler(
        request: Request,
        exc: NotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ConflictError)
    async def conflict_exception_handler(
        request: Request,
        exc: ConflictError,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )