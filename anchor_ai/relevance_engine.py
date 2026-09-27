"""Conservative multi-stage relevance engine for SIIS sections."""

import re
from typing import List, Set, Tuple
from anchor_ai.models import ParsedSIIS, QueryIntent, SIISSection


class RelevanceEngine:
    """Filters and ranks SIIS sections relevant to the user query."""

    # Explicit noise indicators to prune if query has no matching keywords
    _NOISE_DISCRIMINATORS = [
        ({"kids", "child", "parental"}, {"samsung kids", "kidshome"}),
        ({"fingerprint", "biometric", "screen protector"}, {"fingerprint recognition", "improve accuracy"}),
        ({"keyboard", "input method", "typing"}, {"third-party keyboard", "keyboard issue"}),
        ({"pc", "windows", "laptop", "computer"}, {"project your windows", "windows 10", "windows 11"}),
        ({"camera", "pro video", "shutter"}, {"when using the camera", "video flickering"}),
        ({"secure folder"}, {"transfer secure folder"}),
        ({"locked", "security lock", "password lock"}, {"device locked due to security", "device locked"}),
    ]

    def find_relevant_sections(
        self,
        query_intent: QueryIntent,
        parsed_siis: ParsedSIIS,
        min_relevance_threshold: float = 0.15
    ) -> List[SIISSection]:
        """Identify SIIS sections that contain actionable or diagnostic evidence for the query."""
        if not parsed_siis.sections:
            return []

        # If document has only 1 or 2 sections, retain them
        if len(parsed_siis.sections) <= 2:
            return list(parsed_siis.sections)

        query_tokens = set(query_intent.technical_keywords)
        feature_tokens = set(re.findall(r"\b\w+\b", query_intent.affected_feature.lower()))
        combined_query_tokens = query_tokens | feature_tokens

        scored_sections: List[Tuple[SIISSection, float]] = []

        for section in parsed_siis.sections:
            # Check noise exclusion
            if self._is_unrelated_noise(section, combined_query_tokens):
                continue

            score = self._compute_section_relevance(section, query_intent, combined_query_tokens)
            if score >= min_relevance_threshold or self._is_general_troubleshooting_step(section):
                scored_sections.append((section, score))

        # If filter was too aggressive, fallback to all non-noise sections
        if not scored_sections:
            for section in parsed_siis.sections:
                if not self._is_unrelated_noise(section, combined_query_tokens):
                    scored_sections.append((section, 0.5))

        # Preserve original document ordering among the relevant sections
        relevant_sections = [sec for sec, _ in scored_sections]
        return relevant_sections

    def _compute_section_relevance(
        self,
        section: SIISSection,
        query_intent: QueryIntent,
        query_tokens: Set[str]
    ) -> float:
        """Compute lexical + semantic overlap score between section and query."""
        title_tokens = set(re.findall(r"\b\w+\b", section.title.lower()))
        body_tokens = set(re.findall(r"\b\w+\b", section.raw_text.lower()))

        # Title match has high weight
        title_overlap = len(title_tokens & query_tokens) / max(1, len(title_tokens))
        body_overlap = len(body_tokens & query_tokens) / max(1, len(query_tokens))

        score = (title_overlap * 0.6) + (body_overlap * 0.4)

        # Boost if section contains explicit action steps
        if section.steps:
            score += 0.15

        # Boost if section matches diagnostic intent (e.g. cracked screen -> repair service)
        if "cracked" in query_intent.user_state.lower() and section.is_diagnostic:
            score += 0.35

        # Boost if floating circle / pop-up view matches multi-window section
        if "floating" in query_tokens and any(k in section.title.lower() for k in ["pop-up", "multi window", "app pair", "edge panel"]):
            score += 0.4

        return min(1.0, score)

    def _is_unrelated_noise(self, section: SIISSection, query_tokens: Set[str]) -> bool:
        """Conservative check to filter out completely unrelated sub-topics."""
        sec_title_low = section.title.lower()
        sec_text_low = section.raw_text.lower()

        for required_query_words, noise_signatures in self._NOISE_DISCRIMINATORS:
            # If section text/title matches a specialized noise signature
            if any(sig in sec_title_low or sig in sec_text_low for sig in noise_signatures):
                # But query does NOT contain any of the required related words
                if not any(req in query_tokens for req in required_query_words):
                    return True

        return False

    def _is_general_troubleshooting_step(self, section: SIISSection) -> bool:
        """General device recovery steps (restart, safe mode, damage check) that apply broadly."""
        title_low = section.title.lower()
        general_indicators = [
            "force a restart", "restart your phone", "safe mode", "check for physical damage",
            "attempt to power on", "charge the device", "inspect"
        ]
        return any(ind in title_low for ind in general_indicators)
