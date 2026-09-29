"""Official schema validator service."""

from typing import Any, Dict
from fastapi import HTTPException
from pydantic import ValidationError
from student_kit.schema import ContextDeeplinkResponse


class SchemaValidator:
    """Enforces strict validation against official student_kit/schema.py Pydantic model."""

    @staticmethod
    def validate_or_raise(response: ContextDeeplinkResponse) -> ContextDeeplinkResponse:
        """Validate response against official ContextDeeplinkResponse schema.
        
        Raises HTTP 500 if schema validation fails.
        """
        try:
            if isinstance(response, ContextDeeplinkResponse):
                dumped = response.model_dump()
                validated = ContextDeeplinkResponse.model_validate(dumped)
            elif isinstance(response, dict):
                validated = ContextDeeplinkResponse.model_validate(response)
            else:
                raise ValueError(f"Unexpected response type: {type(response)}")

            return validated
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"SCHEMA_VALIDATION_FAILURE: Final response failed official schema validation: {str(exc)}"
            ) from exc
