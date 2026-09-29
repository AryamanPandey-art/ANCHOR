"""Error models for ANCHOR Backend API."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Unique error code for identification")
    message: str = Field(..., description="Human-readable error description")
    details: Optional[Any] = Field(default=None, description="Optional diagnostic details")


class HTTPErrorResponse(BaseModel):
    error: ErrorDetail
