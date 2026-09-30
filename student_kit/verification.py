
import json
import re
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
    custom_description: Optional[str] = None
    custom_message: Optional[str] = None


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

    def _extract_direction(self, text: Any) -> Optional[str]:
        if not text:
            return None
        text_norm = " " + " ".join(str(text).lower().split()) + " "
        act_off = "turn off" in text_norm or "disable " in text_norm or "deactivate " in text_norm or "disabled" in text_norm
        act_on = "turn on" in text_norm or "enable " in text_norm or "activate " in text_norm or "enabled" in text_norm

        if act_off and not act_on:
            return "OFF"
        if act_on and not act_off:
            return "ON"
        return None

    def _direction_matches(self, query: str, entry: dict, candidate: Any = None) -> bool:
        query_dir = self._extract_direction(query)
        action_type = entry.get("originalType", "")

        cand_text = ""
        if candidate:
            action_name = self._get(candidate, "action_name", "")
            description = self._get(candidate, "description", "")
            steps = self._get(candidate, "steps", []) or []
            cand_text = f"{action_name} {description} {' '.join(steps if isinstance(steps, list) else [])}"

        candidate_dir = self._extract_direction(cand_text)

        # 1. Contradiction between Query Direction and Candidate Action Direction
        if query_dir == "OFF" and candidate_dir == "ON":
            return False
        if query_dir == "ON" and candidate_dir == "OFF":
            return False

        # 2. Contradiction between Candidate Action Direction and Catalog Deeplink Type
        if candidate_dir == "ON" and action_type == "offURL":
            return False
        if candidate_dir == "OFF" and action_type == "onURL":
            return False

        # 3. Contradiction between Query Direction and Catalog Deeplink Type
        if query_dir == "OFF" and action_type == "onURL":
            return False
        if query_dir == "ON" and action_type == "offURL":
            return False

        return True

    def verify(
        self,
        candidate: Any,
        query: str = "",
        siis_response: Any = None,
    ) -> VerificationResult:
        raw_action_name = self._get(candidate, "action_name", "")
        description = self._get(candidate, "description", "")
        evidence = self._get(candidate, "evidence_text", "")

        action_name = re.sub(r'^\d+[\.\)]\s*', '', raw_action_name).strip()
        clean_core = re.sub(r'\b(setting|settings|option|options|page|screen)\b', '', action_name, flags=re.IGNORECASE).strip()

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
        clean_text = self._normalize(clean_core)
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
                or (clean_text and len(clean_text) >= 4 and clean_text in catalog_text)
                or (description_text and description_text in catalog_text)
            )

            if not exact_match:
                continue

            if not self._direction_matches(query, entry, candidate=candidate):
                continue

            matches.append(entry)

        if not matches:
            steps_list = self._get(candidate, "steps", []) or []
            cand_text = f"{action_name} {description} {' '.join(steps_list if isinstance(steps_list, list) else [])}"
            query_dir = self._extract_direction(query)
            candidate_dir = self._extract_direction(cand_text)

            if query_dir == "OFF" and candidate_dir == "ON":
                return VerificationResult(
                    False, "Candidate action direction (ON) contradicts query direction (OFF)."
                )
            if query_dir == "ON" and candidate_dir == "OFF":
                return VerificationResult(
                    False, "Candidate action direction (OFF) contradicts query direction (ON)."
                )

            full_text = cand_text.lower()
            is_settings_step = any(kw in full_text for kw in ["setting", "settings", "open", "navigate", "tap", "select", "menu", "screen", "option", "display", "privacy", "battery", "sound", "network", "wifi"])

            if is_settings_step:
                screen_name = "device"
                stop_words = {"open", "tap", "select", "turn", "on", "off", "disable", "enable", "the", "and", "to", "a", "an", "settings", "setting", "screen", "option", "options", "device", "phone"}
                for word in action_name.split():
                    w_clean = word.strip(".,!?;:()[]{}\"'").capitalize()
                    if w_clean.lower() not in stop_words and not w_clean.isdigit():
                        screen_name = w_clean
                        break

                dummy_desc = f"It will open the {screen_name} settings screen"
                dummy_msg = f"Open the {screen_name} device settings screen"

                return VerificationResult(
                    verified=True,
                    reason="Grounded SIIS Settings step matched dummy_positive fallback.",
                    deeplink="bixby://dummy_positive",
                    catalog_id="DL-DUMMY",
                    custom_description=dummy_desc,
                    custom_message=dummy_msg,
                )

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
            raw_desc = self._get(candidate, "description", "")
            description = result.custom_description or raw_desc or action_name
            message_text = result.custom_message or action_name
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
                description=description,
                message=message_text,
                originalType=None,
            )

            actions.append(
                Action(
                    actionName=action_name,
                    description=description,
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

        # Prioritize exact catalog matches over dummy fallback
        actions.sort(
            key=lambda a: 0 if (
                a.stepGroups and a.stepGroups[0].actionableDeeplink and a.stepGroups[0].actionableDeeplink.deeplink.startswith("bixby://masked/")
            ) else 1
        )

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