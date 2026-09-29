
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass
class VerificationResult:
    verified: bool
    reason: str
    deeplink: Optional[str] = None
    validation_deeplink: Optional[str] = None
    catalog_id: Optional[str] = None


class ActionVerifier:
    def __init__(self, catalog_path: Optional[str] = None):
        if catalog_path is None:
            catalog_path = Path(__file__).parent / "deeplinks.json"

        with open(catalog_path, "r", encoding="utf-8") as file:
            catalog = json.load(file)

        self.deeplinks = catalog.get("deeplinks", [])

    @staticmethod
    def _get(action: Any, key: str, default=None):
        if isinstance(action, dict):
            return action.get(key, default)
        return getattr(action, key, default)

    @staticmethod
    def _normalize(text: Any) -> str:
        return " ".join(str(text or "").lower().split())

    @staticmethod
    def _words(text: Any) -> set:
        return set(
            word.strip(".,!?;:()[]{}\"'")
            for word in str(text or "").lower().split()
            if word.strip(".,!?;:()[]{}\"'")
        )

    def _direction_matches(self, query: str, entry: dict) -> bool:
        query = self._normalize(query)
        action_type = entry.get("originalType", "")

        # Determine whether the request explicitly asks to turn
        # a setting on or off.
        words = self._words(query)

        wants_on = (
            "enable" in words
            or "activate" in words
            or "on" in words
            or "turn on" in query
        )

        wants_off = (
            "disable" in words
            or "deactivate" in words
            or "off" in words
            or "turn off" in query
        )

        if wants_on and wants_off:
            return False

        if action_type == "onURL" and wants_off:
            return False

        if action_type == "offURL" and wants_on:
            return False

        return True

    def verify(
        self,
        candidate: Any,
        query: str = "",
        siis_response: Any = None,
    ) -> VerificationResult:
        action_name = self._get(candidate, "action_name", "")
        description = self._get(candidate, "description", "")
        evidence = self._get(candidate, "evidence_text", "")
        source_title = self._get(candidate, "source_section_title", "")

        if not action_name and not description:
            return VerificationResult(
                False, "Candidate has no action name or description."
            )

        if not evidence:
            return VerificationResult(
                False, "Candidate has no supporting evidence."
            )

        # Check evidence against SIIS text when supplied.
        if siis_response is not None:
            if isinstance(siis_response, str):
                siis_text = siis_response
            else:
                siis_text = json.dumps(
                    siis_response, ensure_ascii=False, default=str
                )

            if self._normalize(evidence) not in self._normalize(siis_text):
                return VerificationResult(
                    False,
                    "Evidence was not found in the SIIS response.",
                )

        # Use action name and description to identify a catalog entry.
        action_text = self._normalize(action_name)
        description_text = self._normalize(description)

        if not action_text and not description_text:
            return VerificationResult(
                False, "Candidate has no searchable action details."
            )

        matches = []

        for entry in self.deeplinks:
            catalog_text = self._normalize(
                " ".join(
                    str(entry.get(field, "") or "")
                    for field in (
                        "description",
                        "message",
                        "qna_description",
                    )
                )
            )

            # Require a meaningful exact phrase match.
            # Do not accept a match based only on shared words.
            exact_match = (
                (action_text and action_text in catalog_text)
                or (description_text and description_text in catalog_text)
            )

            if not exact_match:
                continue

            if not self._direction_matches(query, entry):
                continue

            matches.append(entry)

        if not matches:
            return VerificationResult(
                False,
                "No matching catalog entry found for this action.",
            )

        # If several entries match, do not guess which one is correct.
        unique_ids = {entry.get("id") for entry in matches}

        if len(unique_ids) > 1:
            return VerificationResult(
                False,
                "Multiple catalog entries matched; manual disambiguation is needed.",
            )

        entry = matches[0]
        validation = entry.get("validation") or {}

        deeplink = entry.get("deeplink")
        if not deeplink:
            return VerificationResult(
                False, "Matching catalog entry has no deeplink."
            )

        return VerificationResult(
            verified=True,
            reason="Evidence and catalog match found.",
            deeplink=deeplink,
            validation_deeplink=validation.get("deeplink"),
            catalog_id=entry.get("id"),
        )