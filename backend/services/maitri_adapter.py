"""Adapter wrapping Maitri's ActionVerifier implementation."""

from typing import Any, Dict, List, Optional
from student_kit.verification import ActionVerifier, VerificationResult
from student_kit.schema import ContextDeeplinkResponse
from anchor_ai.models import IntelligenceResult
from backend.cache.memory_cache import get_cache


class MaitriAdapter:
    """Adapter bridging anchor_ai IntelligenceResult and Maitri's ActionVerifier."""

    def __init__(self, verifier: Optional[ActionVerifier] = None):
        if verifier is not None:
            self.verifier = verifier
        else:
            self.verifier = get_cache().verifier or ActionVerifier()

    def verify_candidate(
        self,
        candidate: Any,
        query: str = "",
        siis_response: Any = None
    ) -> VerificationResult:
        """Call Maitri's single candidate verification logic."""
        return self.verifier.verify(
            candidate=candidate,
            query=query,
            siis_response=siis_response
        )

    def verify_intelligence(
        self,
        intelligence_result: IntelligenceResult
    ) -> ContextDeeplinkResponse:
        """Pass full IntelligenceResult into Maitri's verify_intelligence facade."""
        # Convert Pydantic object or dict if needed for compatibility
        if hasattr(intelligence_result, "model_dump"):
            data = intelligence_result.model_dump()
        else:
            data = intelligence_result

        return self.verifier.verify_intelligence(data)
