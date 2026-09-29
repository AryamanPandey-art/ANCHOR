"""Safety and direction validator for deeplinks."""

from typing import Any, Dict, Optional, Set
from backend.cache.memory_cache import MemoryCache, get_cache
from student_kit.schema import ContextDeeplinkResponse, Deeplink, ValidationDeepLink


class DeeplinkValidator:
    def __init__(self, cache: Optional[MemoryCache] = None):
        self.cache = cache or get_cache()

    @staticmethod
    def is_external_url(url: Optional[str]) -> bool:
        if not url:
            return False
        normalized = url.strip().lower()
        return (
            normalized.startswith("http://")
            or normalized.startswith("https://")
            or normalized.startswith("ftp://")
            or normalized.startswith("www.")
        )

    def is_valid_catalog_uri(self, uri: Optional[str]) -> bool:
        if not uri:
            return False
        if self.is_external_url(uri):
            return False
        return self.cache.is_valid_deeplink(uri)

    @staticmethod
    def _words(text: str) -> set:
        return {
            word.strip(".,!?;:()[]{}\"'")
            for word in text.lower().split()
            if word.strip(".,!?;:()[]{}\"'")
        }

    def is_direction_mismatch(self, query: str, deeplink_obj: Any) -> bool:
        """Check for ON/OFF request direction conflicts."""
        if not query or not deeplink_obj:
            return False

        words = self._words(query)
        wants_on = bool({"enable", "activate", "enabled", "activated"} & words) or "turn on" in query.lower()
        wants_off = bool({"disable", "deactivate", "disabled", "deactivated"} & words) or "turn off" in query.lower()

        if wants_on and wants_off:
            return False

        original_type = getattr(deeplink_obj, "originalType", None)
        if isinstance(deeplink_obj, dict):
            original_type = deeplink_obj.get("originalType")

        if original_type == "onURL" and wants_off:
            return True
        if original_type == "offURL" and wants_on:
            return True

        return False

    def sanitize_response(
        self,
        response: ContextDeeplinkResponse,
        query: str = ""
    ) -> ContextDeeplinkResponse:
        """Filter out or nullify non-catalog / arbitrary / direction-mismatched deeplinks."""
        for goal in response.contexts:
            for action in goal.actions:
                for step_group in action.stepGroups:
                    # 1. Validate Actionable Deeplink
                    if step_group.actionableDeeplink:
                        act_uri = step_group.actionableDeeplink.deeplink
                        if not self.is_valid_catalog_uri(act_uri) or self.is_direction_mismatch(query, step_group.actionableDeeplink):
                            step_group.actionableDeeplink = None

                    # 2. Validate Validation Deeplink
                    if step_group.validationDeeplink:
                        val_uri = step_group.validationDeeplink.deeplink
                        if not self.is_valid_catalog_uri(val_uri) or self.is_direction_mismatch(query, step_group.validationDeeplink):
                            step_group.validationDeeplink = None

        return response
