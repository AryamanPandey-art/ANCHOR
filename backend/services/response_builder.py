"""Dedicated response builder for ANCHOR Backend."""

from typing import Any, Dict, List, Optional
from student_kit.schema import (
    Action,
    actionCategory,
    ContextDeeplinkResponse,
    Deeplink,
    Goal,
    StepGroup,
    ValidationDeepLink,
)


class ResponseBuilder:
    """Builds and refines ContextDeeplinkResponse from verified pipeline results."""

    @staticmethod
    def build_empty_response() -> ContextDeeplinkResponse:
        """Produce valid ContextDeeplinkResponse with empty contexts."""
        return ContextDeeplinkResponse(contexts=[])

    @staticmethod
    def build_response(
        goal_text: str,
        title: str,
        actions: List[Action],
        score: float = 1.0
    ) -> ContextDeeplinkResponse:
        """Construct ContextDeeplinkResponse given goals and verified actions."""
        if not actions:
            return ContextDeeplinkResponse(contexts=[])

        goal_obj = Goal(
            goal=goal_text or title or "Troubleshooting Steps",
            title=title or "Troubleshooting",
            actions=actions,
            score=round(score, 4)
        )
        return ContextDeeplinkResponse(contexts=[goal_obj])
