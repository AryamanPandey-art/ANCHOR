"""FastAPI application entrypoint for ANCHOR Backend."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from backend.api.health import router as health_router
from backend.api.troubleshoot import router as troubleshoot_router
from backend.cache.memory_cache import get_cache
from backend.models.error import HTTPErrorResponse, ErrorDetail


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load static catalogs and engines on startup."""
    cache = get_cache()
    cache.load()
    yield


app = FastAPI(
    title="ANCHOR Guided Troubleshooting Engine Backend",
    description="Samsung PRISM Hackathon 3.0 Backend Implementation",
    version="1.0.0",
    lifespan=lifespan,
)


from fastapi.encoders import jsonable_encoder

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom handler for request validation failures (HTTP 422)."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "UNPROCESSABLE_ENTITY",
                "message": "Invalid request payload format or validation failure.",
                "details": jsonable_encoder(exc.errors())
            }
        }
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Custom handler for Pydantic validation errors (HTTP 422)."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "UNPROCESSABLE_ENTITY",
                "message": "Validation error in payload fields.",
                "details": jsonable_encoder(exc.errors())
            }
        }
    )


app.include_router(health_router)
app.include_router(troubleshoot_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
