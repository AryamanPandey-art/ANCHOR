"""Pipeline Orchestrator connecting all components end-to-end."""

import logging
from typing import Any, Dict, Optional
from fastapi import HTTPException

from backend.models.request import TroubleshootRequest
from backend.validators.request_validator import RequestValidator
from backend.validators.deeplink_validator import DeeplinkValidator
from backend.services.intelligence_service import IntelligenceService
from backend.services.maitri_adapter import MaitriAdapter
from backend.services.response_builder import ResponseBuilder
from backend.services.schema_validator import SchemaValidator
from student_kit.schema import ContextDeeplinkResponse

logger = logging.getLogger("backend.pipeline")


class PipelineOrchestrator:
    """Orchestrates end-to-end troubleshooting pipeline."""

    def __init__(
        self,
        intelligence_service: Optional[IntelligenceService] = None,
        maitri_adapter: Optional[MaitriAdapter] = None,
        deeplink_validator: Optional[DeeplinkValidator] = None,
    ):
        self.intelligence_service = intelligence_service or IntelligenceService()
        self.maitri_adapter = maitri_adapter or MaitriAdapter()
        self.deeplink_validator = deeplink_validator or DeeplinkValidator()

    def process(self, request: TroubleshootRequest) -> ContextDeeplinkResponse:
        """Run complete troubleshooting pipeline."""
        try:
            # 1. Request Validation
            RequestValidator.validate(request)

            # 2. Run anchor_ai Intelligence Engine
            siis_payload = {
                "title": request.siis_response.title,
                "content": request.siis_response.content
            }
            intel_result = self.intelligence_service.process_query(
                query=request.query,
                siis_response=siis_payload
            )

            # 3. Check if relevant sections or candidate actions exist
            if not intel_result.relevant_sections or not intel_result.candidate_actions:
                empty_resp = ResponseBuilder.build_empty_response()
                return SchemaValidator.validate_or_raise(empty_resp)

            # 4. Run Maitri Verification & Deeplink Resolution
            raw_response = self.maitri_adapter.verify_intelligence(intel_result)

            if not raw_response or not raw_response.contexts:
                empty_resp = ResponseBuilder.build_empty_response()
                return SchemaValidator.validate_or_raise(empty_resp)

            # 5. Deeplink Safety Validation & Direction Enforcement
            sanitized_response = self.deeplink_validator.sanitize_response(
                response=raw_response,
                query=request.query
            )

            # 6. Final Official Schema Validation
            final_response = SchemaValidator.validate_or_raise(sanitized_response)

            return final_response

        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("Unexpected pipeline failure: %s", str(exc))
            raise HTTPException(
                status_code=500,
                detail=f"PIPELINE_EXECUTION_FAILURE: Unexpected error during troubleshooting pipeline execution: {str(exc)}"
            ) from exc
