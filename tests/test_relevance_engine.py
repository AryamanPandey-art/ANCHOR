"""Unit tests for RelevanceEngine and noise rejection."""

import json
import pytest
from anchor_ai.query_parser import QueryParser
from anchor_ai.relevance_engine import RelevanceEngine
from anchor_ai.siis_parser import SIISParser


@pytest.fixture
def relevance_suite():
    return {
        "query_parser": QueryParser(),
        "siis_parser": SIISParser(),
        "engine": RelevanceEngine()
    }


def test_noise_pruning_row_3(relevance_suite):
    # Row 3 contains noise sections: Fingerprint, Samsung Kids PIN, Lock due to security, 3rd party keyboard
    with open("student_kit/siis_responses.json") as f:
        data = json.load(f)
    
    row3 = next(r for r in data["responses"] if r["id"] == "row_3")
    query = row3["original_query"]
    siis = row3["siis_response"]

    parsed_query = relevance_suite["query_parser"].parse(query)
    parsed_siis = relevance_suite["siis_parser"].parse(siis)

    # Initial parsed sections include noise
    all_titles = [s.title for s in parsed_siis.sections]
    assert any("Samsung Kids" in t for t in all_titles)
    assert any("Fingerprint" in t for t in all_titles)

    # Relevance filtering
    relevant = relevance_suite["engine"].find_relevant_sections(parsed_query, parsed_siis)
    relevant_titles = [s.title for s in relevant]

    # Verify noise was pruned
    assert not any("Samsung Kids" in t for t in relevant_titles), "Samsung Kids section should be pruned"
    assert not any("Fingerprint" in t for t in relevant_titles), "Fingerprint section should be pruned"
    assert not any("Third-Party Keyboard" in t for t in relevant_titles), "Keyboard section should be pruned"

    # Verify primary section remains
    assert len(relevant) >= 1
    assert "check first" in relevant[0].raw_text.lower() or "usb mouse" in relevant[0].raw_text.lower()


def test_relevance_retains_step_sections(relevance_suite):
    with open("student_kit/siis_responses.json") as f:
        data = json.load(f)
    
    row1 = next(r for r in data["responses"] if r["id"] == "row_1")
    parsed_query = relevance_suite["query_parser"].parse(row1["original_query"])
    parsed_siis = relevance_suite["siis_parser"].parse(row1["siis_response"])

    relevant = relevance_suite["engine"].find_relevant_sections(parsed_query, parsed_siis)
    assert len(relevant) >= 3
    relevant_titles = [s.title for s in relevant]
    assert any("Clear the Email App" in t for t in relevant_titles)
    assert any("Safe Mode" in t for t in relevant_titles)
