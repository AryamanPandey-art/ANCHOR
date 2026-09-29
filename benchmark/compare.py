"""Comparison utility for benchmark metrics across runs."""

from typing import Any, Dict, Optional
from benchmark.metrics import BenchmarkSummary


class BenchmarkComparator:
    @staticmethod
    def compare(run_a: BenchmarkSummary, run_b: BenchmarkSummary) -> Dict[str, Any]:
        """Compare two benchmark summaries and report diffs."""
        return {
            "queries_diff": run_b.total_queries - run_a.total_queries,
            "schema_validity_diff_pct": round(run_b.schema_validity_pct - run_a.schema_validity_pct, 2),
            "verified_actions_diff": run_b.total_verified_actions - run_a.total_verified_actions,
            "resolved_deeplinks_diff": run_b.total_resolved_deeplinks - run_a.total_resolved_deeplinks,
            "latency_diff_ms": round(run_b.avg_latency_ms - run_a.avg_latency_ms, 2),
            "url_leakage_diff": run_b.total_url_leakages - run_a.total_url_leakages,
        }
