"""Orchestrator for the ANCHOR AI / Intelligence Layer."""

import logging
import time
from typing import Any, Dict, List, Optional
from anchor_ai.action_extractor import ActionExtractor
from anchor_ai.llm_client import LLMClient
from anchor_ai.models import (
    CandidateAction,
    IntelligenceResult,
    ParsedSIIS,
    QueryIntent,
    SIISSection,
)
from anchor_ai.query_parser import QueryParser
from anchor_ai.relevance_engine import RelevanceEngine
from anchor_ai.siis_parser import SIISParser

logger = logging.getLogger("anchor_ai.engine")


class IntelligenceEngine:
    """Primary facade for the ANCHOR Intelligence Layer.
    
    Coordinates query understanding, SIIS parsing, conservative relevance filtering,
    and grounded candidate action extraction.
    """

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        enable_llm: bool = True
    ):
        self.query_parser = QueryParser()
        self.siis_parser = SIISParser()
        self.relevance_engine = RelevanceEngine()
        self.action_extractor = ActionExtractor()
        self.llm_client = llm_client if llm_client is not None else LLMClient()
        self.enable_llm = enable_llm

    def parse_query(self, query: str) -> QueryIntent:
        """Extract intent, state, feature, and direction from user query."""
        return self.query_parser.parse(query)

    def parse_siis(self, siis_response: Dict[str, Any]) -> ParsedSIIS:
        """Parse raw SIIS response into a structured AST of sections and steps."""
        return self.siis_parser.parse(siis_response)

    def find_relevant_evidence(
        self,
        query_intent: QueryIntent,
        parsed_siis: ParsedSIIS
    ) -> List[SIISSection]:
        """Filter SIIS sections to retain only relevant troubleshooting evidence."""
        return self.relevance_engine.find_relevant_sections(query_intent, parsed_siis)

    def extract_candidate_actions(
        self,
        query_intent: QueryIntent,
        relevant_sections: List[SIISSection]
    ) -> List[CandidateAction]:
        """Extract grounded candidate actions from relevant SIIS sections."""
        return self.action_extractor.extract_deterministic_candidates(
            query_intent=query_intent,
            relevant_sections=relevant_sections
        )

    def run_intelligence(
        self,
        query: str,
        siis_response: Dict[str, Any]
    ) -> IntelligenceResult:
        """Execute the full intelligence pipeline and produce an IntelligenceResult for Maitri.
        
        Guarantees:
        1. Query intent, state, and direction are extracted.
        2. SIIS document is parsed into structured sections.
        3. Relevant sections are isolated and noise is pruned.
        4. Grounded candidate actions are proposed with explicit provenance.
        5. Seamless fallback to deterministic execution if LLM fails or is disabled.
        """
        start_time = time.time()
        fallback_used = False
        llm_data: Optional[Dict[str, Any]] = None

        # 1. Deterministic Query Parsing
        query_intent = self.parse_query(query)

        # 2. Deterministic SIIS Parsing
        parsed_siis = self.parse_siis(siis_response)

        # 3. Multi-Stage Relevance Filtering
        relevant_sections = self.find_relevant_evidence(query_intent, parsed_siis)

        # 4. Extract Deterministic Candidates (Baseline Ground Truth)
        deterministic_candidates = self.extract_candidate_actions(query_intent, relevant_sections)

        # 5. Optional LLM Semantic Refinement (if enabled and available)
        if self.enable_llm and self.llm_client and self.llm_client.is_available():
            section_texts = [sec.raw_text for sec in relevant_sections]
            llm_data = self.llm_client.extract_structured_intelligence(
                query=query,
                siis_title=parsed_siis.title,
                section_texts=section_texts
            )

        if llm_data:
            candidate_actions = self.action_extractor.merge_or_refine_candidates(
                deterministic_candidates=deterministic_candidates,
                llm_response=llm_data,
                parsed_sections=relevant_sections
            )
            # Update query intent direction if LLM provided higher-confidence direction
            llm_intent = llm_data.get("query_intent", {})
            if isinstance(llm_intent, dict) and "direction" in llm_intent:
                dir_val = str(llm_intent["direction"]).upper()
                if dir_val in ("ON", "OFF") and query_intent.direction.value == "null":
                    from anchor_ai.models import Direction
                    query_intent.direction = Direction[dir_val]
        else:
            fallback_used = True
            candidate_actions = deterministic_candidates

        latency_ms = round((time.time() - start_time) * 1000, 2)

        return IntelligenceResult(
            query_intent=query_intent,
            parsed_siis=parsed_siis,
            relevant_sections=relevant_sections,
            candidate_actions=candidate_actions,
            fallback_used=fallback_used,
            metadata={
                "latency_ms": latency_ms,
                "sections_total": len(parsed_siis.sections),
                "sections_relevant": len(relevant_sections),
                "candidate_count": len(candidate_actions),
                "engine_version": "1.0.0-prism",
                "llm_used": bool(llm_data)
            }
        )
