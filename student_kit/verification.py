
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from student_kit.schema import (
    Action,
    actionCategory,
    ContextDeeplinkResponse,
    Deeplink,
    Goal,
    StepGroup,
    ValidationDeepLink,
)


@dataclass
class VerificationResult:
    verified: bool
    reason: str
    deeplink: Optional[str] = None
    validation_deeplink: Optional[str] = None
    catalog_id: Optional[str] = None
    validation_key: Optional[str] = None


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
        return {
            word.strip(".,!?;:()[]{}\"'")
            for word in str(text or "").lower().split()
            if word.strip(".,!?;:()[]{}\"'")
        }

    def _direction_matches(self, query: str, entry: dict) -> bool:
        query = self._normalize(query)
        words = self._words(query)
        action_type = entry.get("originalType", "")

        wants_on = bool(
            {"enable", "activate", "enabled", "activated"} & words
        ) or "turn on" in query

        wants_off = bool(
            {"disable", "deactivate", "disabled", "deactivated"} & words
        ) or "turn off" in query

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

        if not action_name and not description:
            return VerificationResult(
                False, "Candidate has no action name or description."
            )

        if not evidence:
            return VerificationResult(
                False, "Candidate has no supporting evidence."
            )

        if siis_response is not None:
            if isinstance(siis_response, str):
                siis_text = siis_response
            elif hasattr(siis_response, "model_dump"):
                siis_text = json.dumps(
                    siis_response.model_dump(),
                    ensure_ascii=False,
                    default=str,
                )
            else:
                siis_text = json.dumps(
                    siis_response, ensure_ascii=False, default=str
                )

            if self._normalize(evidence) not in self._normalize(siis_text):
                return VerificationResult(
                    False, "Evidence was not found in the SIIS response."
                )

        action_text = self._normalize(action_name)
        description_text = self._normalize(description)
        matches = []

        for entry in self.deeplinks:
            catalog_text = self._normalize(
                " ".join(
                    str(entry.get(field, "") or "")
                    for field in (
                        "description",
                        "message",
                        "qna_description",
                        "originalType",
                    )
                )
            )

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
                False, "No matching catalog entry found for this action."
            )

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
            validation_key=validation.get("key"),
            catalog_id=entry.get("id"),
        )

    def verify_intelligence(
        self,
        intelligence_result: Any,
    ) -> ContextDeeplinkResponse:
        """Verify all candidates and convert verified ones to the public schema."""
        intent = self._get(intelligence_result, "query_intent")
        parsed_siis = self._get(intelligence_result, "parsed_siis")
        candidates = self._get(
            intelligence_result, "candidate_actions", []
        ) or []

        query = self._get(intent, "intent_summary", "")
        direction = self._get(intent, "direction", None)

        if direction and str(getattr(direction, "value", direction)).lower() != "null":
            query = f"{query} {getattr(direction, 'value', direction)}"

        siis_response = self._get(parsed_siis, "raw_content", None)

        actions = []
        scores = []

        for candidate in candidates:
            result = self.verify(
                candidate,
                query=query,
                siis_response=siis_response,
            )

            if not result.verified:
                continue

            action_name = self._get(candidate, "action_name", "")
            description = self._get(candidate, "description", "")
            steps = self._get(candidate, "steps", []) or []
            category = self._get(candidate, "category_hint", "manual")
            confidence = self._get(candidate, "confidence", 1.0)

            validation = None
            if result.validation_deeplink and result.validation_key:
                validation = ValidationDeepLink(
                    deeplink=result.validation_deeplink,
                    key=result.validation_key,
                )

            actionable = Deeplink(
                deeplink=result.deeplink,
                description=description or action_name,
                message=action_name,
                originalType=None,
            )

            actions.append(
                Action(
                    actionName=action_name,
                    description=description or action_name,
                    category=actionCategory(category),
                    stepGroups=[
                        StepGroup(
                            steps=steps,
                            validationDeeplink=validation,
                            actionableDeeplink=actionable,
                        )
                    ],
                )
            )
            scores.append(float(confidence))

        if not actions:
            return ContextDeeplinkResponse(contexts=[])

        title = self._get(parsed_siis, "title", "") or "Troubleshooting"
        goal_text = self._get(intent, "intent_summary", "") or title

        return ContextDeeplinkResponse(
            contexts=[
                Goal(
                    goal=goal_text,
                    title=title,
                    actions=actions,
                    score=sum(scores) / len(scores),
                )
            ]
        )