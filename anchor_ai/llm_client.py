"""Isolated LLM client wrapper for ANCHOR AI Layer."""

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional
from anchor_ai.models import CandidateAction, Direction, QueryIntent

logger = logging.getLogger("anchor_ai.llm")


class LLMClient:
    """Provides structured LLM interpretation with graceful fallback."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
        timeout_sec: float = 10.0
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        self.timeout_sec = timeout_sec

    def is_available(self) -> bool:
        """Check if an API key is configured."""
        return bool(self.api_key)

    def extract_structured_intelligence(
        self,
        query: str,
        siis_title: str,
        section_texts: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Call LLM with structured prompt. Returns parsed JSON dict or None on failure."""
        if not self.is_available():
            logger.debug("No LLM API key configured. Skipping LLM call.")
            return None

        prompt = self._build_prompt(query, siis_title, section_texts)

        try:
            raw_response = self._call_gemini_rest_api(prompt)
            if not raw_response:
                return None

            cleaned_json = self._clean_json_markdown(raw_response)
            parsed_data = json.loads(cleaned_json)
            return parsed_data
        except Exception as e:
            logger.warning(f"LLM extraction failed or timed out: {e}. Falling back to deterministic pipeline.")
            return None

    def _build_prompt(self, query: str, siis_title: str, section_texts: List[str]) -> str:
        """Build strict structured prompt enforcing SIIS evidence grounding."""
        siis_context = "\n\n---\n\n".join(section_texts)
        return f"""You are the Intelligence Layer for ANCHOR, a proof-carrying troubleshooting engine for Samsung devices.

TASK:
Extract the user intent and candidate troubleshooting actions from the provided SIIS technical text for the given user query.

STRICT GROUNDING RULES:
1. Derive candidate actions ONLY from the provided SIIS text.
2. NEVER invent steps, menu paths, settings, or deeplinks not explicitly in the SIIS text.
3. Preserve original step ordering when specified.
4. Distinguish user direction accurately: "ON", "OFF", or "null".
5. Return ONLY a valid JSON object matching the schema below.

USER QUERY:
"{query}"

SIIS ARTICLE TITLE:
"{siis_title}"

SIIS EVIDENCE TEXT:
{siis_context}

OUTPUT JSON SCHEMA:
{{
  "query_intent": {{
    "intent_summary": "string",
    "affected_feature": "string",
    "user_state": "string",
    "direction": "ON" | "OFF" | "null",
    "technical_keywords": ["string"]
  }},
  "candidate_actions": [
    {{
      "action_name": "string",
      "description": "string",
      "steps": ["step 1", "step 2"],
      "source_section_title": "string",
      "evidence_text": "string",
      "category_hint": "auto" | "manual" | "critical"
    }}
  ]
}}
"""

    def _call_gemini_rest_api(self, prompt: str) -> Optional[str]:
        """Call Gemini REST API directly with standard library to avoid external package locks."""
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json"
            }
        }

        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
            if resp.status == 200:
                result = json.loads(resp.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    return text
        return None

    def _clean_json_markdown(self, raw_text: str) -> str:
        """Strip ```json markdown wrappers if present."""
        text = raw_text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        return text
