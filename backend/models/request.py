"""Request models and Pydantic validators for ANCHOR Backend API."""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class SIISPayload(BaseModel):
    """SIIS Knowledge Store response payload."""
    title: str = Field(..., description="SIIS document title")
    content: str = Field(..., description="SIIS verbatim markdown or text content")

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if v is None or not str(v).strip():
            raise ValueError("SIIS title must be a non-empty string.")
        return v.strip()

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if v is None or not str(v).strip():
            raise ValueError("SIIS content must be a non-empty string.")
        return v.strip()


class TroubleshootRequest(BaseModel):
    """Incoming POST /v1/troubleshoot request payload."""
    query: str = Field(..., description="User troubleshooting query")
    siis_response: SIISPayload = Field(..., description="SIIS knowledge response payload")
    row_id: Optional[str] = Field(default=None, description="Optional evaluation row ID")

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        if v is None or not str(v).strip():
            raise ValueError("Query must be a non-empty string.")
        return v.strip()
