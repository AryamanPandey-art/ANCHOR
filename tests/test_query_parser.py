"""Unit tests for QueryParser."""

import pytest
from anchor_ai.models import Direction
from anchor_ai.query_parser import QueryParser


@pytest.fixture
def parser():
    return QueryParser()


def test_direction_off_queries(parser):
    test_cases = [
        ("Turn off touch sensitivity", Direction.OFF),
        ("My Galaxy S25 has a floating circle... I want to remove it.", Direction.OFF),
        ("Disable full screen gestures on my phone", Direction.OFF),
        ("Stop screen mirroring immediately", Direction.OFF),
        ("Close split screen mode", Direction.OFF),
    ]
    for query, expected_dir in test_cases:
        res = parser.parse(query)
        assert res.direction == expected_dir, f"Failed on query: {query}"


def test_direction_on_queries(parser):
    test_cases = [
        ("Enable touch sensitivity on Galaxy S24", Direction.ON),
        ("Turn on auto rotate", Direction.ON),
        ("Switch on Smart View mirroring", Direction.ON),
        ("Activate safe mode", Direction.ON),
    ]
    for query, expected_dir in test_cases:
        res = parser.parse(query)
        assert res.direction == expected_dir, f"Failed on query: {query}"


def test_direction_none_queries(parser):
    test_cases = [
        ("My Samsung A115G tablet screen flashes and then goes completely blank", Direction.NONE),
        ("My Galaxy phone's screen is completely cracked, it's a total crack", Direction.NONE),
        ("My Galaxy S22 screen inputs are delayed and the touch responsiveness is laggy", Direction.NONE),
        ("My Galaxy Flip 6 screen is half black", Direction.NONE),
    ]
    for query, expected_dir in test_cases:
        res = parser.parse(query)
        assert res.direction == expected_dir, f"Failed on query: {query}"


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
