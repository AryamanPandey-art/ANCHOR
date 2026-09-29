# ⚓ ANCHOR Backend & Evaluation Layer

The Backend & Evaluation module for **ANCHOR** (Smart Guided Troubleshooting Engine for Samsung Galaxy Devices).

This package orchestrates the end-to-end troubleshooting pipeline, integrating the frozen `anchor_ai` intelligence layer, Maitri's `ActionVerifier` & deeplink resolution module, strict deeplink safety validation, and official Samsung response schema enforcement.

---

## 🏗 Architecture & Pipeline

```
User Query + SIIS Response
           │
           ▼
  POST /v1/troubleshoot
           │
           ▼
  Request Validation (RequestValidator)
           │
           ▼
  anchor_ai IntelligenceEngine (Candidate Actions)
           │
           ▼
  Maitri Verification Adapter (MaitriAdapter)
           │
           ▼
  Deeplink Safety & Direction Sanitizer (DeeplinkValidator)
           │
           ▼
  Response Builder (ResponseBuilder)
           │
           ▼
  Official Schema Validation (SchemaValidator)
           │
           ▼
  ContextDeeplinkResponse JSON
```

---

## 📁 Package Structure

```
backend/
├── __init__.py
├── main.py                  # FastAPI application entrypoint & error handlers
├── README.md                # Backend documentation
├── api/
│   ├── __init__.py
│   ├── health.py            # GET /health
│   └── troubleshoot.py      # POST /v1/troubleshoot
├── cache/
│   ├── __init__.py
│   └── memory_cache.py      # In-memory catalog loader & engine singleton
├── models/
│   ├── __init__.py
│   ├── request.py           # Request payloads & Pydantic field validators
│   ├── catalog.py           # Catalog data models
│   ├── error.py             # Error response schemas
│   └── internal.py          # Internal pipeline representations
├── pipeline/
│   ├── __init__.py
│   └── orchestrator.py      # End-to-end pipeline orchestrator
├── services/
│   ├── __init__.py
│   ├── intelligence_service.py # anchor_ai engine wrapper
│   ├── maitri_adapter.py       # Maitri ActionVerifier adapter
│   ├── response_builder.py     # Schema response builder
│   └── schema_validator.py     # Official Pydantic schema validator
├── validators/
│   ├── __init__.py
│   ├── request_validator.py    # Request validation logic
│   └── deeplink_validator.py   # Catalog URI & direction safety validator
└── tests/
    ├── __init__.py
    └── test_backend.py      # Comprehensive 21-scenario unit & integration tests

benchmark/
├── __init__.py
├── metrics.py               # Metric models & aggregators
├── compare.py               # Benchmark comparison utility
└── run_benchmark.py         # 20-row SIIS dataset evaluation runner
```

---

## 🚀 Running the Backend

### Start Server Locally
```bash
python -m backend.main
```
Or using Uvicorn directly:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📡 API Reference

### 1. `GET /health`
Returns the status and version of the backend service.

**Response `200 OK`**:
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### 2. `POST /v1/troubleshoot`
Processes a user troubleshooting query alongside an official SIIS knowledge store payload.

**Request Payload**:
```json
{
  "query": "Switch Time Format",
  "siis_response": {
    "title": "Time Format",
    "content": "Switches between 12-hour and 24-hour time format to display time in your preferred style."
  },
  "row_id": "optional_id"
}
```

**Response `200 OK`**:
Conforms strictly to `student_kit/schema.py` (`ContextDeeplinkResponse`).

---

## 🧪 Running Tests

Execute the complete test suite (41 tests):
```bash
python -m pytest backend/tests/ tests/
```

---

## 📊 Running the Evaluation Benchmark

Run evaluation across the official 20-row SIIS dataset:
```bash
python -m benchmark.run_benchmark
```
Reports total queries, schema validity %, candidate actions, verified actions, resolved deeplinks, direction mismatches, URL leakage, and average latency.
