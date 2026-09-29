"""Health check router."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}
