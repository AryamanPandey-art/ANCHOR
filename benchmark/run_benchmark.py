"""Run evaluation benchmark across official 20-row SIIS dataset."""

import json
import time
from pathlib import Path
from typing import List

from backend.cache.memory_cache import get_cache
from backend.models.request import TroubleshootRequest, SIISPayload
from backend.pipeline.orchestrator import PipelineOrchestrator
from backend.validators.deeplink_validator import DeeplinkValidator
from benchmark.metrics import BenchmarkRowMetric, BenchmarkSummary
from student_kit.schema import ContextDeeplinkResponse


def run_benchmark(output_path: Optional[Path] = None) -> BenchmarkSummary:
    """Execute evaluation benchmark over official siis_responses.json."""
    cache = get_cache()
    cache.load()

    dataset_path = Path(__file__).parent.parent / "student_kit" / "siis_responses.json"
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    responses = data.get("responses", [])
    orchestrator = PipelineOrchestrator()
    deeplink_validator = DeeplinkValidator(cache=cache)

    row_metrics: List[BenchmarkRowMetric] = []
    total_latency = 0.0

    print(f"\n=======================================================")
    print(f"[BENCHMARK] ANCHOR BACKEND BENCHMARK - Evaluating {len(responses)} SIIS Rows")
    print(f"=======================================================\n")

    for i, row in enumerate(responses, start=1):
        row_id = row.get("id", f"row_{i}")
        query = row.get("original_query", "")
        siis_raw = row.get("siis_response", {})
        siis_title = siis_raw.get("title", "")
        siis_content = siis_raw.get("content", "")

        t0 = time.time()
        metric = BenchmarkRowMetric(
            row_id=row_id,
            original_query=query,
            siis_title=siis_title
        )

        try:
            req = TroubleshootRequest(
                query=query,
                siis_response=SIISPayload(title=siis_title, content=siis_content),
                row_id=row_id
            )

            # 1. Run anchor_ai intelligence
            intel_result = orchestrator.intelligence_service.process_query(
                query=query,
                siis_response={"title": siis_title, "content": siis_content}
            )
            metric.candidate_count = len(intel_result.candidate_actions)
            metric.fallback_used = intel_result.fallback_used

            # 2. Run Maitri verification
            verification_resp = orchestrator.maitri_adapter.verify_intelligence(intel_result)

            # 3. Process sanitized response
            final_resp = orchestrator.deeplink_validator.sanitize_response(verification_resp, query=query)
            ContextDeeplinkResponse.model_validate(final_resp.model_dump())
            metric.schema_valid = True

            # Metrics collection
            verified_count = 0
            resolved_dl_count = 0
            direction_mismatches = 0
            url_leakage = False

            for goal in final_resp.contexts:
                for action in goal.actions:
                    verified_count += 1
                    for step_group in action.stepGroups:
                        if step_group.actionableDeeplink:
                            uri = step_group.actionableDeeplink.deeplink
                            resolved_dl_count += 1
                            if deeplink_validator.is_external_url(uri):
                                url_leakage = True
                            if deeplink_validator.is_direction_mismatch(query, step_group.actionableDeeplink):
                                direction_mismatches += 1

                        if step_group.validationDeeplink:
                            val_uri = step_group.validationDeeplink.deeplink
                            resolved_dl_count += 1
                            if deeplink_validator.is_external_url(val_uri):
                                url_leakage = True
                            if deeplink_validator.is_direction_mismatch(query, step_group.validationDeeplink):
                                direction_mismatches += 1

            metric.verified_action_count = verified_count
            metric.rejected_action_count = max(0, metric.candidate_count - verified_count)
            metric.resolved_deeplink_count = resolved_dl_count
            metric.direction_mismatch_count = direction_mismatches
            metric.url_leakage_detected = url_leakage

        except Exception as exc:
            metric.schema_valid = False
            metric.error = str(exc)

        latency_ms = round((time.time() - t0) * 1000, 2)
        metric.latency_ms = latency_ms
        total_latency += latency_ms
        row_metrics.append(metric)

        status_str = "PASS" if metric.schema_valid else "FAIL"
        print(f"Row {i:2d}/{len(responses)} [{row_id}]: {status_str} | Candidates: {metric.candidate_count:2d} | Verified: {metric.verified_action_count:2d} | DLs: {metric.resolved_deeplink_count:2d} | Latency: {latency_ms:6.2f}ms")

    # Aggregate Summary
    total_queries = len(row_metrics)
    schema_valid_count = sum(1 for m in row_metrics if m.schema_valid)
    total_candidates = sum(m.candidate_count for m in row_metrics)
    total_verified = sum(m.verified_action_count for m in row_metrics)
    total_rejected = sum(m.rejected_action_count for m in row_metrics)
    total_resolved_dls = sum(m.resolved_deeplink_count for m in row_metrics)
    total_direction_mismatches = sum(m.direction_mismatch_count for m in row_metrics)
    total_url_leakages = sum(1 for m in row_metrics if m.url_leakage_detected)
    avg_latency = round(total_latency / max(1, total_queries), 2)
    fallback_count = sum(1 for m in row_metrics if m.fallback_used)

    summary = BenchmarkSummary(
        total_queries=total_queries,
        schema_valid_responses=schema_valid_count,
        total_candidates=total_candidates,
        total_verified_actions=total_verified,
        total_rejected_actions=total_rejected,
        total_resolved_deeplinks=total_resolved_dls,
        total_direction_mismatches=total_direction_mismatches,
        total_url_leakages=total_url_leakages,
        avg_latency_ms=avg_latency,
        anchor_ai_fallback_count=fallback_count,
        schema_validity_pct=round((schema_valid_count / max(1, total_queries)) * 100, 2),
        deeplink_resolution_pct=round((total_resolved_dls / max(1, total_verified * 2)) * 100, 2) if total_verified > 0 else 0.0
    )

    print(f"\n=======================================================")
    print(f"[SUMMARY] BENCHMARK SUMMARY REPORT")
    print(f"=======================================================")
    print(f"Total Queries Evaluated:        {summary.total_queries}")
    print(f"Schema-Valid Responses:         {summary.schema_valid_responses} ({summary.schema_validity_pct}%)")
    print(f"Candidate Actions Proposed:    {summary.total_candidates}")
    print(f"Verified Actions Approved:      {summary.total_verified_actions}")
    print(f"Rejected Actions Filtered:     {summary.total_rejected_actions}")
    print(f"Resolved Catalog Deeplinks:     {summary.total_resolved_deeplinks}")
    print(f"Direction Mismatches:          {summary.total_direction_mismatches}")
    print(f"External URL Leakages:         {summary.total_url_leakages}")
    print(f"Average Pipeline Latency:       {summary.avg_latency_ms} ms")
    print(f"anchor_ai Fallback Used:       {summary.anchor_ai_fallback_count}")
    print(f"=======================================================\n")

    if output_path:
        report_data = {
            "summary": summary.model_dump(),
            "rows": [m.model_dump() for m in row_metrics]
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        print(f"Report saved to: {output_path}")

    return summary


if __name__ == "__main__":
    out_file = Path(__file__).parent / "benchmark_report.json"
    run_benchmark(output_path=out_file)
