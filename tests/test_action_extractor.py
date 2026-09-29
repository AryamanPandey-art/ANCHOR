"""Unit tests for ActionExtractor, provenance, and fallback behavior."""

import pytest
from anchor_ai.action_extractor import ActionExtractor
from anchor_ai.models import Direction, QueryIntent, SIISSection


@pytest.fixture
def extractor():
    return ActionExtractor()


def test_deterministic_action_extraction(extractor):
    section = SIISSection(
        section_id="sec_4",
        title="Step 4: Clear the Email App's Cache and Data",
        header_level=2,
        raw_text=(
            "To clear the app's cache:\n"
            "Navigate to Settings.\n"
            "Tap Apps.\n"
            "Select your email app.\n"
            "Tap Storage.\n"
            "Tap Clear cache."
        ),
        steps=[
            "Navigate to Settings.",
            "Tap Apps.",
            "Select your email app.",
            "Tap Storage.",
            "Tap Clear cache."
        ],
        is_actionable=True
    )
    query_intent = QueryIntent(
        intent_summary="Clear email cache",
        affected_feature="Email Connection & Account",
        user_state="Email app crashing",
        direction=Direction.NONE,
        technical_keywords=["email", "cache", "clear"]
    )

    candidates = extractor.extract_deterministic_candidates(query_intent, [section])
    assert len(candidates) == 1
    act = candidates[0]

    assert "Clear" in act.action_name
    assert act.source_section_id == "sec_4"
    assert act.source_section_title == "Step 4: Clear the Email App's Cache and Data"
    assert len(act.steps) == 5
    assert act.category_hint == "auto"
    assert act.confidence >= 0.8
    assert act.provenance["grounded"] is True


def test_zero_hallucination_step_grounding(extractor):
    section = SIISSection(
        section_id="sec_2",
        title="Force a Restart",
        header_level=3,
        raw_text="Press and hold Power and Volume down for 20 seconds.",
        steps=["Press and hold Power and Volume down for 20 seconds."]
    )
    query_intent = QueryIntent(
        intent_summary="Restart device",
        affected_feature="Display & Screen Power",
        user_state="Screen black",
        direction=Direction.NONE
    )

    candidates = extractor.extract_deterministic_candidates(query_intent, [section])
    for cand in candidates:
        for step in cand.steps:
            # Step must exist in raw text
            assert step.lower() in section.raw_text.lower() or any(w in section.raw_text.lower() for w in step.lower().split())


def test_llm_fallback_on_malformed_response(extractor):
    section = SIISSection(
        section_id="sec_1",
        title="Check Internet",
        header_level=2,
        raw_text="Ensure phone is connected to Wi-Fi. Go to Settings, tap Connections.",
        steps=["Go to Settings, tap Connections."]
    )
    query_intent = QueryIntent(
        intent_summary="Check Wi-Fi",
        affected_feature="Connections",
        user_state="No network",
        direction=Direction.NONE
    )
    deterministic_candidates = extractor.extract_deterministic_candidates(query_intent, [section])

    # Case 1: Malformed dictionary
    res1 = extractor.merge_or_refine_candidates(
        deterministic_candidates=deterministic_candidates,
        llm_response={"invalid_key": 123},
        parsed_sections=[section]
    )
    assert len(res1) == len(deterministic_candidates)
    assert res1[0].action_name == deterministic_candidates[0].action_name

    # Case 2: None response
    res2 = extractor.merge_or_refine_candidates(
        deterministic_candidates=deterministic_candidates,
        llm_response=None,
        parsed_sections=[section]
    )
    assert len(res2) == len(deterministic_candidates)
