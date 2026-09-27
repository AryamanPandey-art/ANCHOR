"""Candidate action extractor grounded in SIIS evidence."""

import re
from typing import Any, Dict, List, Optional
from anchor_ai.models import CandidateAction, Direction, QueryIntent, SIISSection


class ActionExtractor:
    """Extracts candidate troubleshooting actions grounded strictly in SIIS sections."""

    def extract_deterministic_candidates(
        self,
        query_intent: QueryIntent,
        relevant_sections: List[SIISSection]
    ) -> List[CandidateAction]:
        """Extract candidate actions deterministically from parsed SIIS sections."""
        candidates: List[CandidateAction] = []

        for section in relevant_sections:
            action = self._create_candidate_from_section(section, query_intent)
            if action:
                candidates.append(action)

        return candidates

    def merge_or_refine_candidates(
        self,
        deterministic_candidates: List[CandidateAction],
        llm_response: Optional[Dict[str, Any]],
        parsed_sections: List[SIISSection]
    ) -> List[CandidateAction]:
        """Verify LLM candidate actions against SIIS ground truth or fallback to deterministic candidates."""
        if not llm_response or "candidate_actions" not in llm_response:
            return deterministic_candidates

        raw_llm_actions = llm_response.get("candidate_actions", [])
        if not isinstance(raw_llm_actions, list) or len(raw_llm_actions) == 0:
            return deterministic_candidates

        section_map = {sec.title.lower(): sec for sec in parsed_sections}
        section_id_map = {sec.section_id: sec for sec in parsed_sections}
        full_text_lower = " ".join([sec.raw_text.lower() for sec in parsed_sections])

        verified_candidates: List[CandidateAction] = []

        for raw in raw_llm_actions:
            if not isinstance(raw, dict):
                continue

            action_name = str(raw.get("action_name", "")).strip()
            description = str(raw.get("description", "")).strip()
            steps = raw.get("steps", [])
            source_title = str(raw.get("source_section_title", "")).strip()
            evidence_text = str(raw.get("evidence_text", "")).strip()
            category_hint = raw.get("category_hint", "manual")
            if category_hint not in ("auto", "manual", "critical"):
                category_hint = "manual"

            if not action_name:
                continue

            # Grounding check: verify that evidence exists in SIIS
            matching_section = (
                section_map.get(source_title.lower()) or
                self._fuzzy_find_section(source_title, parsed_sections)
            )

            if matching_section:
                sec_id = matching_section.section_id
                sec_title = matching_section.title
                # If LLM didn't provide steps or altered them, prefer SIIS extracted steps
                final_steps = (
                    [str(s).strip() for s in steps if str(s).strip()]
                    if steps and self._verify_steps_grounding(steps, matching_section.raw_text)
                    else matching_section.steps
                )
                final_evidence = evidence_text if (evidence_text.lower() in matching_section.raw_text.lower()) else matching_section.raw_text[:300]
            else:
                # Fallback to closest section
                if not parsed_sections:
                    continue
                sec_id = parsed_sections[0].section_id
                sec_title = parsed_sections[0].title
                final_steps = [str(s).strip() for s in steps if str(s).strip()]
                final_evidence = evidence_text or parsed_sections[0].raw_text[:200]

            conf = self._compute_confidence(final_steps, final_evidence, full_text_lower)

            verified_candidates.append(
                CandidateAction(
                    action_name=action_name,
                    description=description or f"Troubleshooting step for {action_name}",
                    steps=final_steps,
                    source_section_title=sec_title,
                    source_section_id=sec_id,
                    evidence_text=final_evidence,
                    category_hint=category_hint,
                    confidence=conf,
                    provenance={
                        "source_section_id": sec_id,
                        "source_section_title": sec_title,
                        "llm_extracted": True,
                        "grounded": True,
                        "step_count": len(final_steps)
                    }
                )
            )

        return verified_candidates if verified_candidates else deterministic_candidates

    def _create_candidate_from_section(
        self,
        section: SIISSection,
        query_intent: QueryIntent
    ) -> Optional[CandidateAction]:
        """Convert a single SIISSection into a grounded CandidateAction."""
        clean_title = re.sub(r"^(?:Step\s+\d+:|###?\s*\d+\.?|#+)\s*", "", section.title).strip()
        if not clean_title:
            clean_title = "Perform Troubleshooting Step"

        # Determine description from section body
        first_sentence = self._extract_first_sentence(section.raw_text)
        description = first_sentence if first_sentence else f"Follow procedural steps for {clean_title}."

        # Detect category hint (auto for Settings navigation sequences, manual otherwise)
        is_auto = any("settings" in s.lower() or "tap" in s.lower() for s in section.steps)
        category_hint = "auto" if is_auto else "manual"

        # Determine evidence text
        evidence_text = section.raw_text[:300].strip()

        # Compute confidence score
        confidence = self._compute_confidence(section.steps, evidence_text, section.raw_text.lower())

        return CandidateAction(
            action_name=clean_title,
            description=description,
            steps=section.steps if section.steps else [clean_title],
            source_section_title=section.title,
            source_section_id=section.section_id,
            evidence_text=evidence_text,
            category_hint=category_hint,
            confidence=confidence,
            provenance={
                "source_section_id": section.section_id,
                "source_section_title": section.title,
                "llm_extracted": False,
                "grounded": True,
                "step_count": len(section.steps)
            }
        )

    def _extract_first_sentence(self, text: str) -> str:
        """Extract the first descriptive sentence from a section body."""
        lines = [line.strip() for line in text.split("\n") if line.strip() and not line.strip().startswith("#")]
        if not lines:
            return ""
        first_line = lines[0]
        match = re.match(r"^([^.!?]+[.!?])", first_line)
        if match:
            return match.group(1).strip()
        return first_line[:120].strip()

    def _verify_steps_grounding(self, steps: List[Any], section_text: str) -> bool:
        """Verify that at least 50% of key words in steps appear in the section text."""
        sec_text_low = section_text.lower()
        matched = 0
        total = 0
        for step in steps:
            words = [w.lower() for w in re.findall(r"\b\w{4,}\b", str(step))]
            if not words:
                continue
            total += 1
            if any(w in sec_text_low for w in words):
                matched += 1
        return (matched / max(1, total)) >= 0.5

    def _fuzzy_find_section(self, title: str, sections: List[SIISSection]) -> Optional[SIISSection]:
        """Match section by title similarity."""
        title_words = set(re.findall(r"\b\w{3,}\b", title.lower()))
        best_sec = None
        best_score = 0.0
        for sec in sections:
            sec_words = set(re.findall(r"\b\w{3,}\b", sec.title.lower()))
            overlap = len(title_words & sec_words) / max(1, len(title_words))
            if overlap > best_score and overlap > 0.3:
                best_score = overlap
                best_sec = sec
        return best_sec

    def _compute_confidence(self, steps: List[str], evidence: str, base_text: str) -> float:
        """Deterministic confidence score calculation."""
        score = 0.70  # Baseline confidence for grounded candidate

        if len(steps) >= 2:
            score += 0.15
        elif len(steps) == 1:
            score += 0.05

        if len(evidence) > 40 and evidence.lower() in base_text:
            score += 0.15

        return min(1.0, round(score, 2))
