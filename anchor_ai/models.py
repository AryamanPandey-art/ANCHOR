"""Data models for the ANCHOR Intelligence Layer."""

from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class Direction(str, Enum):
    """User intent direction for toggles/settings."""
    ON = "ON"
    OFF = "OFF"
    NONE = "null"


class QueryIntent(BaseModel):
    """Structured extraction of user troubleshooting query."""
    intent_summary: str = Field(description="Summary of what the user is trying to troubleshoot or accomplish")
    affected_feature: str = Field(description="The primary setting, feature, or component involved (e.g. Display, Wi-Fi, Touch)")
    user_state: str = Field(description="The failure state, symptom, or condition reported by the user")
    direction: Direction = Field(default=Direction.NONE, description="Target direction: ON, OFF, or null if unspecified")
    technical_keywords: List[str] = Field(default_factory=list, description="Extracted domain keywords")
    device_model: Optional[str] = Field(default=None, description="Extracted Galaxy / Samsung device model if present")


class SIISSection(BaseModel):
    """Structured representation of a parsed SIIS section."""
    section_id: str = Field(description="Unique identifier for the section in the document")
    title: str = Field(description="Section heading or step title")
    header_level: int = Field(default=2, description="Markdown header level (1-4)")
    raw_text: str = Field(description="Full verbatim text of the section")
    steps: List[str] = Field(default_factory=list, description="Extracted procedural steps in order")
    is_actionable: bool = Field(default=True, description="Whether section contains device settings/actions")
    is_diagnostic: bool = Field(default=False, description="Whether section is diagnostic/service check")


class ParsedSIIS(BaseModel):
    """Structured AST representation of raw SIIS response."""
    title: str = Field(description="Title of the SIIS article")
    applicability: Optional[str] = Field(default=None, description="Applicable devices header")
    sections: List[SIISSection] = Field(default_factory=list, description="Ordered sections parsed from SIIS content")
    raw_content: str = Field(description="Original unparsed SIIS content")


class CandidateAction(BaseModel):
    """Candidate troubleshooting action extracted from SIIS evidence."""
    action_name: str = Field(description="Concise name for the troubleshooting action")
    description: str = Field(description="Brief explanation of why this action helps or what it does")
    steps: List[str] = Field(default_factory=list, description="Sequential execution steps extracted strictly from SIIS evidence")
    source_section_title: str = Field(description="Title of the source SIIS section providing evidence")
    source_section_id: str = Field(description="ID of the source SIIS section")
    evidence_text: str = Field(description="Verbatim or grounded snippet from SIIS supporting this action")
    category_hint: Literal["auto", "manual", "critical"] = Field(
        default="manual",
        description="Suggested action category based on procedural characteristics"
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Deterministic heuristic confidence score based on grounding match ratio"
    )
    provenance: Dict[str, Any] = Field(
        default_factory=dict,
        description="Detailed provenance metadata (e.g. source line range, exact match flag)"
    )


class IntelligenceResult(BaseModel):
    """Internal output interface passed to Maitri's Verification & Deeplink Layer."""
    query_intent: QueryIntent = Field(description="Extracted query intent, state, and direction")
    parsed_siis: ParsedSIIS = Field(description="Parsed structured SIIS document")
    relevant_sections: List[SIISSection] = Field(description="SIIS sections determined to be relevant to the query")
    candidate_actions: List[CandidateAction] = Field(description="Ordered candidate actions grounded in SIIS evidence")
    fallback_used: bool = Field(default=False, description="Whether deterministic fallback was triggered")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Execution metrics, latency, and debug info")
