"""Benchmark metrics tracking module for ANCHOR Backend evaluation."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LatencyPercentiles(BaseModel):
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    mean_ms: float = 0.0
    max_ms: float = 0.0
    count: int = 0


class CacheEvaluationPhase(BaseModel):
    phase_name: str
    total_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    hit_rate_pct: float = 0.0
    percentiles: LatencyPercentiles = Field(default_factory=LatencyPercentiles)


class BenchmarkRowMetric(BaseModel):
    row_id: str
    original_query: str
    siis_title: str
    schema_valid: bool = False
    candidate_count: int = 0
    verified_action_count: int = 0
    rejected_action_count: int = 0
    resolved_deeplink_count: int = 0
    direction_mismatch_count: int = 0
    url_leakage_detected: bool = False
    latency_ms: float = 0.0
    fallback_used: bool = False
    error: Optional[str] = None


class BenchmarkSummary(BaseModel):
    total_queries: int = 0
    schema_valid_responses: int = 0
    total_candidates: int = 0
    total_verified_actions: int = 0
    total_rejected_actions: int = 0
    total_resolved_deeplinks: int = 0
    total_direction_mismatches: int = 0
    total_url_leakages: int = 0
    avg_latency_ms: float = 0.0
    anchor_ai_fallback_count: int = 0
    schema_validity_pct: float = 0.0
    deeplink_resolution_pct: float = 0.0

    # Official A3 Cache & Latency Benchmarks
    cold_phase: Optional[CacheEvaluationPhase] = None
    repeat_phase: Optional[CacheEvaluationPhase] = None
    paraphrase_phase: Optional[CacheEvaluationPhase] = None

