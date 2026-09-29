"""Service wrapping the frozen anchor_ai IntelligenceEngine."""

from typing import Any, Dict, Optional
from anchor_ai.engine import IntelligenceEngine
from anchor_ai.models import IntelligenceResult
from backend.cache.memory_cache import get_cache


class IntelligenceService:
    def __init__(self, engine: Optional[IntelligenceEngine] = None):
        if engine is not None:
            self.engine = engine
        else:
            self.engine = get_cache().engine or IntelligenceEngine(enable_llm=False)

    def process_query(self, query: str, siis_response: Dict[str, Any]) -> IntelligenceResult:
        """Run the frozen intelligence engine on query and SIIS response."""
        return self.engine.run_intelligence(
            query=query,
            siis_response=siis_response
        )
