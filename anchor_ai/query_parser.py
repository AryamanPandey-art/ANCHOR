"""Deterministic and rule-guided query intent parser for ANCHOR."""

import re
from typing import List, Optional, Tuple
from anchor_ai.models import Direction, QueryIntent


class QueryParser:
    """Extracts technical intent, affected feature, state, and direction from user queries."""

    # Device pattern
    _DEVICE_PATTERN = re.compile(
        r"\b((?:Samsung\s+|Galaxy\s+)(?:Z\s+Flip\s*\d+|Z\s+Fold\s*\d+|S\d+\s*Ultra|S\d+\s*\+?|A\d+(?:/\s*A\d+)?|[A-Za-z0-9*+-]+(?:\s+tablet|\s+phone)?))\b",
        re.IGNORECASE
    )

    # Direction patterns
    _OFF_PATTERNS = [
        r"\b(?:turn\s+off|turnoff|switch\s+off|switchoff)\b",
        r"\b(?:disable|deactivate|stop|prevent)\b",
        r"\b(?:remove|delete|get\s+rid\s+of|close|exit|dismiss)\b",
        r"\b(?:don['’]?t\s+want|wants?\s+to\s+remove|turn\s+it\s+off)\b",
    ]
    _ON_PATTERNS = [
        r"\b(?:turn\s+on|turnon|switch\s+on|switchon)\b",
        r"\b(?:enable|activate|start|resume)\b",
        r"\b(?:turn\s+it\s+on|wants?\s+to\s+enable)\b",
    ]

    # Feature mapping rules
    _FEATURE_RULES = [
        (r"\b(?:touch\s+sensitiv|touch\s+respons|laggy|delayed\s+input|touch\s+not\s+working)\b", "Touchscreen & Sensitivity"),
        (r"\b(?:floating\s+circle|pop-?up\s+view|multi\s*window|split\s*screen|app\s*pairs?|edge\s*panel)\b", "Multi Window & Pop-up View"),
        (r"\b(?:smart\s*view|mirroring|casting|screen\s*mirror|stream\s*to\s*tv|aspect\s*ratio)\b", "Smart View & Screen Mirroring"),
        (r"\b(?:smart\s*switch|secure\s*folder|transfer\s*(?:my\s*)?data|qr\s*code)\b", "Data Transfer & Smart Switch"),
        (r"\b(?:email|gmail|mail\s*server|email\s*account)\b", "Email Connection & Account"),
        (r"\b(?:cracked|crack|broken\s*screen|shattered|bleeding\s*pixels?|ink\s*blots?)\b", "Screen Physical Damage"),
        (r"\b(?:rotat|auto-?rotate|portrait|landscape)\b", "Screen Auto Rotate"),
        (r"\b(?:bright|dim|dark\s*screen|dark\s*mode|eye\s*comfort)\b", "Display & Brightness"),
        (r"\b(?:flash(?:es|ing)?|flicker(?:s|ing)?|blue\s*screen|blank\s*screen|black\s*screen|won['’]?t\s*turn\s*on)\b", "Display & Screen Power"),
    ]

    def parse(self, query: str) -> QueryIntent:
        """Parse natural language query into a structured QueryIntent object."""
        clean_query = self._sanitize_query(query)
        device = self._extract_device(clean_query)
        direction = self._extract_direction(clean_query)
        feature = self._extract_feature(clean_query)
        state = self._extract_state(clean_query)
        keywords = self._extract_keywords(clean_query)
        intent_summary = self._generate_intent_summary(clean_query, feature, direction, state)

        return QueryIntent(
            intent_summary=intent_summary,
            affected_feature=feature,
            user_state=state,
            direction=direction,
            technical_keywords=keywords,
            device_model=device
        )

    def _sanitize_query(self, query: str) -> str:
        """Strip numbering prefixes, quotes, and excess whitespace."""
        # e.g. 1. "My Galaxy S24..." -> My Galaxy S24...
        cleaned = re.sub(r"^\s*\d+[.)]\s*", "", query)
        cleaned = cleaned.strip("\"' \t\n\r")
        return cleaned

    def _extract_device(self, query: str) -> Optional[str]:
        """Extract Samsung Galaxy device model name."""
        match = self._DEVICE_PATTERN.search(query)
        if match:
            return match.group(1).strip()
        return None

    def _extract_direction(self, query: str) -> Direction:
        """Determine if query is an explicit ON/OFF command or symptom report."""
        low = query.lower()

        # Check OFF patterns first
        for pat in self._OFF_PATTERNS:
            if re.search(pat, low):
                return Direction.OFF

        # Check ON patterns
        for pat in self._ON_PATTERNS:
            if re.search(pat, low):
                return Direction.ON

        return Direction.NONE

    def _extract_feature(self, query: str) -> str:
        """Map query terminology to target device feature."""
        low = query.lower()
        for pattern, feature_name in self._FEATURE_RULES:
            if re.search(pattern, low):
                return feature_name
        return "Display & Device Settings"

    def _extract_state(self, query: str) -> str:
        """Extract the failure symptom or reported user state."""
        low = query.lower()
        symptom_mappings = [
            ("cracked", "Screen physically cracked or damaged"),
            ("flashes", "Screen flashing intermittently"),
            ("flicker", "Screen flickering"),
            ("blank", "Display completely blank or black"),
            ("black", "Display screen black/unresponsive"),
            ("floating circle", "Floating shortcut/pop-up circle appearing on screen"),
            ("laggy", "Delayed touch input and laggy responsiveness"),
            ("delayed", "Delayed touch input and laggy responsiveness"),
            ("responsive", "Touch responsiveness issue"),
            ("not rotating", "Screen rotation not functioning"),
            ("transfer", "Data transfer / Smart Switch blocked"),
            ("email", "Email app connection failing or crashing"),
            ("small", "Display window small and not expanding"),
            ("half black", "Partial screen display failure (half black)"),
            ("distorted", "Screen display distorted after receipt"),
        ]
        for term, desc in symptom_mappings:
            if term in low:
                return desc
        return "Device reporting unexpected display or operational failure"

    def _extract_keywords(self, query: str) -> List[str]:
        """Extract technical search keywords from query."""
        stop_words = {
            "my", "the", "a", "an", "is", "are", "and", "or", "in", "on", "at", "to", "for",
            "of", "with", "it", "its", "so", "that", "this", "when", "whenever", "after",
            "i", "me", "cant", "can't", "cannot", "try", "tried", "even", "though", "phone",
            "device", "new", "short", "time", "again", "works", "happens", "use"
        }
        tokens = re.findall(r"\b[A-Za-z0-9_-]+\b", query.lower())
        return [t for t in tokens if len(t) > 2 and t not in stop_words]

    def _generate_intent_summary(self, query: str, feature: str, direction: Direction, state: str) -> str:
        """Generate high-level summary of intent."""
        if direction == Direction.OFF:
            return f"Disable / remove {feature} in response to '{state}'"
        elif direction == Direction.ON:
            return f"Enable / configure {feature} to resolve issue"
        return f"Troubleshoot {feature} issue: {state}"
