"""Request validation helper."""

from fastapi import HTTPException
from pydantic import ValidationError
from backend.models.request import TroubleshootRequest


class RequestValidator:
    @staticmethod
    def validate(request: TroubleshootRequest) -> None:
        """Validate request payload requirements.
        
        Rules:
        - query exists & non-empty
        - siis_response exists
        - siis_response.title exists & non-empty
        - siis_response.content exists & non-empty
        """
        if not request.query or not request.query.strip():
            raise HTTPException(
                status_code=422,
                detail="Query must be a non-empty string."
            )
        if not request.siis_response:
            raise HTTPException(
                status_code=422,
                detail="siis_response is required."
            )
        if not request.siis_response.title or not request.siis_response.title.strip():
            raise HTTPException(
                status_code=422,
                detail="siis_response.title must be a non-empty string."
            )
        if not request.siis_response.content or not request.siis_response.content.strip():
            raise HTTPException(
                status_code=422,
                detail="siis_response.content must be a non-empty string."
            )
