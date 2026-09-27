"""Unit tests for QueryParser."""

import pytest
from anchor_ai.models import Direction
from anchor_ai.query_parser import QueryParser


@pytest.fixture
def parser():
    return QueryParser()


def test_direction_off_commands(parser):
    test_cases = [
        ("Turn off touch sensitivity", Direction.OFF),
        ("My Galaxy S25 has a floating circle... I want to remove it.", Direction.OFF),
        ("Disable full screen gestures on my phone", Direction.OFF),
        ("Switch off auto rotate", Direction.OFF),
        ("Please deactivate touch sensitivity", Direction.OFF),
    ]
    for query, expected_dir in test_cases:
        res = parser.parse(query)
        assert res.direction == expected_dir, f"Failed on command query: {query}"


def test_direction_on_commands(parser):
    test_cases = [
        ("Enable touch sensitivity on Galaxy S24", Direction.ON),
        ("Turn on auto rotate", Direction.ON),
        ("Switch on Smart View mirroring", Direction.ON),
        ("Activate safe mode", Direction.ON),
        ("I want to enable touch sensitivity", Direction.ON),
    ]
    for query, expected_dir in test_cases:
        res = parser.parse(query)
        assert res.direction == expected_dir, f"Failed on command query: {query}"


def test_symptom_phrases_do_not_trigger_direction_on(parser):
    """Ensure symptom failure phrases with 'turn on' are NOT treated as Direction.ON."""
    symptom_cases = [
        "My Galaxy S24 Ultra screen is completely black and won't turn on",
        "It doesn't display anything, even when I try to turn it on.",
        "My Galaxy S26 Ultra only shows a blue screen when I try to turn it on",
        "My Galaxy S22 screen stays blank when I turn it on after carrier deactivated old phone",
        "My phone fails to turn on after dropping it in water",
        "Unable to turn on my Galaxy tablet",
        "The screen can't turn on at all",
        "Doesn't turn on even with charger plugged in",
    ]
    for query in symptom_cases:
        res = parser.parse(query)
        assert res.direction == Direction.NONE, (
            f"Symptom phrase '{query}' falsely triggered direction {res.direction}"
        )


def test_multi_clause_query_parsing(parser):
    """Verify that multi-symptom numbered queries extract sub_symptoms."""
    query = (
        '1. "My Galaxy Z Flip 7 screen is cracked again right where it folds." '
        '2. "The touch doesn\'t work on certain parts of the screen." '
        '3. "I can hardly see anything on the display."'
    )
    res = parser.parse(query)
    assert len(res.sub_symptoms) == 3
    assert "screen is cracked" in res.sub_symptoms[0]
    assert "touch doesn't work" in res.sub_symptoms[1]
    assert "hardly see anything" in res.sub_symptoms[2]
    assert res.device_model == "Galaxy Z Flip 7"
    assert res.direction == Direction.NONE


def test_device_extraction(parser):
    res1 = parser.parse("My Galaxy S22 screen turns completely blank")
    assert res1.device_model == "Galaxy S22"

    res2 = parser.parse("My Galaxy Z Flip 7 screen went completely black")
    assert res2.device_model == "Galaxy Z Flip 7"

    res3 = parser.parse("My Samsung A115G tablet screen flashes")
    assert "Samsung A115G" in res3.device_model or "tablet" in res3.affected_feature.lower()


def test_feature_and_state_mapping(parser):
    res_touch = parser.parse("My Galaxy S22 touch responsiveness is laggy")
    assert "Touch" in res_touch.affected_feature
    assert "laggy" in res_touch.user_state.lower()

    res_crack = parser.parse("My screen is completely cracked")
    assert "Damage" in res_crack.affected_feature or "Screen" in res_crack.affected_feature
    assert "cracked" in res_crack.user_state.lower()
