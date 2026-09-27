"""Deterministic SIIS Markdown parser for ANCHOR."""

import re
from typing import Any, Dict, List, Optional, Tuple
from anchor_ai.models import ParsedSIIS, SIISSection


class SIISParser:
    """Parses raw SIIS technical documents into structured sections and steps."""

    # Regex to match Markdown headers
    _HEADER_PATTERN = re.compile(r"^(#{1,4})\s+(.+)$", re.MULTILINE)
    
    # Common action verbs for imperative sentence detection
    _ACTION_VERBS = (
        r"(?:Navigate to|Go to|Open|Tap|Select|Touch|Press and hold|Press|Hold|Swipe|Drag|"
        r"Connect|Plug|Disconnect|Turn on|Turn off|Enable|Disable|Remove|Insert|Shine|"
        r"Reinsert|Restart|Reboot|Boot|Check|Verify|Ensure|Examine|Inspect|Confirm|Adjust|"
        r"Clear|Reset|Uninstall|Visit|Contact|Schedule|Provide)"
    )
    _IMPERATIVE_PATTERN = re.compile(
        rf"^\s*(?:[-*•]|\d+[.)])?\s*({_ACTION_VERBS}\b.+?[.!?])(?:\s+|$)",
        re.IGNORECASE | re.MULTILINE
    )

    _DIAGNOSTIC_KEYWORDS = {
        "damage", "liquid", "ldi", "corrosion", "bent pins", "repair", "service center",
        "service", "warranty", "cracked", "ink blots", "bleeding", "inspection", "support"
    }

    def parse(self, siis_data: Dict[str, Any]) -> ParsedSIIS:
        """Parse raw SIIS dictionary into a ParsedSIIS AST object."""
        title = siis_data.get("title", "").strip()
        raw_content = siis_data.get("content", "").strip()

        if not raw_content:
            return ParsedSIIS(title=title, applicability=None, sections=[], raw_content="")

        applicability, cleaned_content = self._extract_applicability(raw_content, title)
        sections = self._extract_sections(cleaned_content, default_title=title)

        return ParsedSIIS(
            title=title,
            applicability=applicability,
            sections=sections,
            raw_content=raw_content
        )

    def _extract_applicability(self, content: str, title: str) -> Tuple[Optional[str], str]:
        """Separate applicability metadata header from markdown body."""
        # Check if content begins with device list e.g. "Smartphone,Others Mobile,... Title ( Smartphone,...):"
        first_line = content.split("\n", 1)[0]
        header_match = re.match(r"^([A-Za-z\s,/]+?)\s+" + re.escape(title[:20]) if title else r"^([A-Za-z\s,/]+?):", first_line)
        
        if header_match:
            # We found a device prefix
            colon_idx = content.find("):")
            if colon_idx != -1 and colon_idx < 300:
                applicability = content[:colon_idx+2].strip()
                remaining = content[colon_idx+2:].strip()
                return applicability, remaining
            else:
                first_colon = content.find(":")
                if first_colon != -1 and first_colon < 200:
                    applicability = content[:first_colon].strip()
                    remaining = content[first_colon+1:].strip()
                    return applicability, remaining

        return None, content

    def _extract_sections(self, content: str, default_title: str) -> List[SIISSection]:
        """Split content by markdown headers and construct SIISSection items."""
        sections: List[SIISSection] = []
        
        # Find all header positions
        matches = list(self._HEADER_PATTERN.finditer(content))
        
        if not matches:
            # No markdown headers found; treat whole text as a single section
            steps = self._extract_steps(content)
            sections.append(
                SIISSection(
                    section_id="sec_1",
                    title=default_title or "General Troubleshooting",
                    header_level=1,
                    raw_text=content,
                    steps=steps,
                    is_actionable=len(steps) > 0,
                    is_diagnostic=self._is_diagnostic_text(content)
                )
            )
            return sections

        # Handle any preamble before the first header
        first_match = matches[0]
        if first_match.start() > 0:
            preamble = content[:first_match.start()].strip()
            if preamble:
                steps = self._extract_steps(preamble)
                sections.append(
                    SIISSection(
                        section_id="sec_0",
                        title=default_title or "Overview / Preliminary Steps",
                        header_level=1,
                        raw_text=preamble,
                        steps=steps,
                        is_actionable=len(steps) > 0,
                        is_diagnostic=self._is_diagnostic_text(preamble)
                    )
                )

        # Process each header section
        for i, match in enumerate(matches):
            header_markup = match.group(1)
            header_title = match.group(2).strip()
            header_level = len(header_markup)
            start_pos = match.end()
            
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            section_body = content[start_pos:end_pos].strip()
            
            # Combine header title and section body for full verbatim text
            full_section_text = f"{header_markup} {header_title}\n{section_body}".strip()
            steps = self._extract_steps(section_body)
            
            is_diag = (
                self._is_diagnostic_text(header_title) or 
                self._is_diagnostic_text(section_body)
            )

            # Skip glossary sections from candidate actions
            if header_title.lower() == "glossary":
                continue

            sections.append(
                SIISSection(
                    section_id=f"sec_{len(sections) + 1}",
                    title=header_title,
                    header_level=header_level,
                    raw_text=full_section_text,
                    steps=steps,
                    is_actionable=len(steps) > 0,
                    is_diagnostic=is_diag
                )
            )

        return sections

    def _extract_steps(self, text: str) -> List[str]:
        """Extract ordered sequential procedural steps from text while preserving exact wording."""
        steps: List[str] = []
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        for line in lines:
            # Check if line is a bullet/numbered item
            clean_line = re.sub(r"^[-*•]\s+|\b\d+[.)]\s+", "", line).strip()
            
            # If line is short and starts with an imperative action verb or setting path
            if self._is_step_line(clean_line):
                # Split compound sentences if they contain multiple distinct step sentences
                sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", clean_line)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence and len(sentence) > 5:
                        steps.append(sentence)
            elif len(clean_line) > 10 and any(keyword in clean_line.lower() for keyword in ["navigate to", "tap", "select", "press and hold", "swipe down"]):
                steps.append(clean_line)

        # Remove duplicate adjacent steps while preserving order
        deduped_steps: List[str] = []
        for step in steps:
            if not deduped_steps or deduped_steps[-1] != step:
                deduped_steps.append(step)

        return deduped_steps

    def _is_step_line(self, line: str) -> bool:
        """Determine if a line represents an executable troubleshooting instruction."""
        if not line:
            return False
        first_word = line.split()[0].rstrip(".,:")
        action_verb_list = {
            "navigate", "go", "open", "tap", "select", "touch", "press", "hold", "swipe", "drag",
            "connect", "plug", "disconnect", "turn", "enable", "disable", "remove", "insert",
            "shine", "reinsert", "restart", "reboot", "boot", "check", "verify", "ensure",
            "examine", "inspect", "confirm", "adjust", "clear", "reset", "uninstall", "visit",
            "contact", "schedule", "provide", "first", "next", "then", "finally", "to"
        }
        return first_word.lower() in action_verb_list

    def _is_diagnostic_text(self, text: str) -> bool:
        """Check if text primarily refers to hardware diagnostics, damage, or service centers."""
        low = text.lower()
        return any(k in low for k in self._DIAGNOSTIC_KEYWORDS)
