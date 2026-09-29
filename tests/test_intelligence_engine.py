"""Integration tests and benchmark evaluation over all 20 official SIIS rows."""

import json
import os
import time
import pytest
from anchor_ai.engine import IntelligenceEngine
from anchor_ai.models import IntelligenceResult


@pytest.fixture
def engine():
    return IntelligenceEngine(enable_llm=False)  # Deterministic baseline benchmark


@pytest.fixture
def siis_dataset():
    path = "student_kit/siis_responses.json"
    assert os.path.exists(path), f"Official SIIS dataset not found at {path}"
    with open(path) as f:
        data = json.load(f)
    return data["responses"]


def test_all_20_siis_rows(engine, siis_dataset):
    """Benchmark test over all 20 official student-kit rows."""
    assert len(siis_dataset) == 20, f"Expected 20 rows, got {len(siis_dataset)}"

    total_candidates = 0
    total_latency_ms = 0.0
    grounding_failures = 0

    for i, row in enumerate(siis_dataset):
        row_id = row["id"]
        query = row["original_query"]
        siis_resp = row["siis_response"]

        start = time.time()
        result: IntelligenceResult = engine.run_intelligence(query, siis_resp)
        elapsed_ms = (time.time() - start) * 1000
        total_latency_ms += elapsed_ms

        # Assertions
        assert result.query_intent is not None, f"Missing query intent for {row_id}"
        assert result.query_intent.affected_feature != "", f"Empty feature for {row_id}"
        assert len(result.relevant_sections) > 0, f"No relevant sections for {row_id}"
        assert len(result.candidate_actions) > 0, f"No candidate actions for {row_id}"

        total_candidates += len(result.candidate_actions)

        # Provenance and Grounding Verification
        for action in result.candidate_actions:
            assert action.action_name != "", f"Empty action name in {row_id}"
            assert action.source_section_title != "", f"Missing source section in {row_id}"
            assert action.evidence_text != "", f"Missing evidence text in {row_id}"
            assert len(action.steps) > 0, f"Empty steps list in {row_id}"

            # Check evidence grounding in raw SIIS text
            if action.evidence_text[:30].lower() not in siis_resp["content"].lower():
                grounding_failures += 1

    avg_latency = total_latency_ms / len(siis_dataset)
    avg_candidates = total_candidates / len(siis_dataset)

    print(f"\n==========================================")
    print(f"BENCHMARK RESULTS OVER {len(siis_dataset)} OFFICIAL ROWS:")
    print(f"Total Candidates Extracted: {total_candidates}")
    print(f"Avg Candidates / Query:     {avg_candidates:.2f}")
    print(f"Avg Processing Latency:     {avg_latency:.2f} ms")
    print(f"Grounding Failure Count:    {grounding_failures}")
    print(f"Grounding Accuracy:         {((total_candidates - grounding_failures) / total_candidates) * 100:.1f}%")
    print(f"==========================================")

    assert grounding_failures == 0, f"Detected {grounding_failures} ungrounded evidence snippets!"
