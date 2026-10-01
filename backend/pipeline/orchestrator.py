"""Pipeline Orchestrator connecting all components end-to-end."""

import logging
from typing import Any, Dict, Optional, Tuple
from fastapi import HTTPException

from backend.cache.memory_cache import MemoryCache, get_cache
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
    """Orchestrates end-to-end troubleshooting pipeline with context-safe caching."""

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
        """Run complete troubleshooting pipeline with context-safe cache lookup and store."""
        final_response, _ = self.process_with_provenance(request)
        return final_response

    def process_with_provenance(
        self,
        request: TroubleshootRequest
    ) -> Tuple[ContextDeeplinkResponse, Optional[Any]]:
        """Run complete troubleshooting pipeline and return both official response and internal intelligence result."""
        try:
            # 1. Request Validation
            RequestValidator.validate(request)

            cache = get_cache()
            siis_title = request.siis_response.title
            siis_content = request.siis_response.content
            siis_hash = MemoryCache.compute_siis_hash(siis_title, siis_content)
            exact_key = MemoryCache.compute_exact_key(siis_hash, request.query)

            # Extract deterministic query intent for direction-aware semantic key
            query_intent = self.intelligence_service.engine.parse_query(request.query)
            semantic_key = MemoryCache.compute_semantic_key(siis_hash, query_intent.direction.value)

            # 3. Always run or parse intelligence to provide provenance metadata
            siis_payload = {
                "title": siis_title,
                "content": siis_content
            }
            intel_result = self.intelligence_service.process_query(
                query=request.query,
                siis_response=siis_payload
            )

            # 2. Check Context-Safe Response Cache
            cached_resp, hit_type = cache.get_cached_response(exact_key, semantic_key)
            if cached_resp is not None:
                if hit_type == "PARAPHRASE_HIT":
                    cache.store_cached_response(exact_key, None, cached_resp)
                return cached_resp, intel_result

            # 4. Check if relevant sections or candidate actions exist
            if not intel_result.relevant_sections or not intel_result.candidate_actions:
                empty_resp = ResponseBuilder.build_empty_response()
                validated_empty = SchemaValidator.validate_or_raise(empty_resp)
                cache.store_cached_response(exact_key, semantic_key, validated_empty)
                return validated_empty, intel_result

            # 5. Run Maitri Verification & Deeplink Resolution
            raw_response = self.maitri_adapter.verify_intelligence(intel_result)

            if not raw_response or not raw_response.contexts:
                empty_resp = ResponseBuilder.build_empty_response()
                validated_empty = SchemaValidator.validate_or_raise(empty_resp)
                cache.store_cached_response(exact_key, semantic_key, validated_empty)
                return validated_empty, intel_result

            # 6. Deeplink Safety Validation & Direction Enforcement
            sanitized_response = self.deeplink_validator.sanitize_response(
                response=raw_response,
                query=request.query
            )

            # 7. Final Official Schema Validation
            final_response = SchemaValidator.validate_or_raise(sanitized_response)

            # 8. Store in Context-Safe Cache
            cache.store_cached_response(exact_key, semantic_key, final_response)

            return final_response, intel_result

        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("Unexpected pipeline failure: %s", str(exc))
            raise HTTPException(
                status_code=500,
                detail=f"PIPELINE_EXECUTION_FAILURE: Unexpected error during troubleshooting pipeline execution: {str(exc)}"
            ) from exc

