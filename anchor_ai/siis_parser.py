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

            # Skip glossary sections from candidate actions
            if header_title.lower() == "glossary":
                continue

            sub_secs = self._split_composite_section_if_needed(
                header_title=header_title,
                header_level=header_level,
                section_body=section_body,
                base_id=f"sec_{len(sections) + 1}"
            )
            sections.extend(sub_secs)

        return sections

    def _split_composite_section_if_needed(
        self,
        header_title: str,
        header_level: int,
        section_body: str,
        base_id: str
    ) -> List[SIISSection]:
        """Split tips or multi-topic sections into discrete granular sub-sections if they contain independent procedures."""
        # Do not split atomic numbered steps e.g. "Step 1: Check Physical Damage", "Step 2: Force a Restart"
        if re.match(r"^Step\s+\d+", header_title, re.IGNORECASE):
            steps = self._extract_steps(section_body)
            is_diag = self._is_diagnostic_text(header_title) or self._is_diagnostic_text(section_body)
            full_text = f"{'#' * header_level} {header_title}\n{section_body}".strip()
            return [
                SIISSection(
                    section_id=base_id,
                    title=header_title,
                    header_level=header_level,
                    raw_text=full_text,
                    steps=steps,
                    is_actionable=len(steps) > 0,
                    is_diagnostic=is_diag
                )
            ]

        paragraphs = [p.strip() for p in section_body.split("\n") if p.strip()]
        
        # Split if section explicitly represents tips/factors or contains multiple independent conditional paragraphs
        is_composite_topic = any(w in header_title.lower() for w in ["tips", "factors", "service options", "understanding", "things to check"])
        has_conditional_paragraphs = sum(1 for p in paragraphs if p.startswith("If ") or re.match(r"^[A-Z][A-Za-z\s]+:", p)) >= 2
        
        if not (is_composite_topic or has_conditional_paragraphs) or len(paragraphs) <= 1:
            steps = self._extract_steps(section_body)
            is_diag = self._is_diagnostic_text(header_title) or self._is_diagnostic_text(section_body)
            full_text = f"{'#' * header_level} {header_title}\n{section_body}".strip()
            return [
                SIISSection(
                    section_id=base_id,
                    title=header_title,
                    header_level=header_level,
                    raw_text=full_text,
                    steps=steps,
                    is_actionable=len(steps) > 0,
                    is_diagnostic=is_diag
                )
            ]


        sub_sections: List[SIISSection] = []
        for j, para in enumerate(paragraphs):
            # Skip mere preamble sentences like "Here are some tips..."
            if j == 0 and len(para) < 100 and ("here are some tips" in para.lower() or "please consider the following" in para.lower()):
                continue

            sub_title = self._derive_sub_title(para, header_title)
            steps = self._extract_steps(para)
            is_diag = self._is_diagnostic_text(sub_title) or self._is_diagnostic_text(para)
            
            sub_sections.append(
                SIISSection(
                    section_id=f"{base_id}_{j+1}",
                    title=sub_title,
                    header_level=header_level + 1,
                    raw_text=para,
                    steps=steps,
                    is_actionable=len(steps) > 0,
                    is_diagnostic=is_diag
                )
            )

        return sub_sections if sub_sections else [
            SIISSection(
                section_id=base_id,
                title=header_title,
                header_level=header_level,
                raw_text=f"{'#' * header_level} {header_title}\n{section_body}".strip(),
                steps=self._extract_steps(section_body),
                is_actionable=True,
                is_diagnostic=self._is_diagnostic_text(header_title)
            )
        ]

    def _derive_sub_title(self, paragraph: str, parent_title: str) -> str:
        """Derive a concise sub-title from a paragraph, retaining parent topic context."""
        colon_match = re.match(r"^([A-Z][A-Za-z0-9\s/]+):", paragraph)
        if colon_match:
            sub = colon_match.group(1).strip()
            return f"{parent_title}: {sub}" if sub.lower() not in parent_title.lower() else sub
        
        # If paragraph starts with "If ..."
        if paragraph.startswith("If "):
            first_sentence = paragraph.split(".")[0].strip()
            sub = first_sentence if len(first_sentence) < 80 else first_sentence[:75].strip() + "..."
            return f"{parent_title} - {sub}"
        
        # If paragraph starts with "On a ..." or "On ..."
        if paragraph.startswith("On "):
            first_sentence = paragraph.split(".")[0].strip()
            sub = first_sentence if len(first_sentence) < 80 else first_sentence[:75].strip() + "..."
            return f"{parent_title} - {sub}"

        first_sentence = paragraph.split(".")[0].strip()
        sub = first_sentence[:60].strip() if len(first_sentence) > 60 else first_sentence
        return f"{parent_title}: {sub}" if sub.lower() not in parent_title.lower() else sub



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
