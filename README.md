# ANCHOR — Proof-Carrying Troubleshooting Engine

> Samsung PRISM Generative AI Hackathon 3.0 — Theme 2: Smart Guided Troubleshooting Engine

## Project Overview

ANCHOR is a **proof-carrying troubleshooting engine** that provides verified, evidence-grounded troubleshooting guidance for Samsung Galaxy device issues. Every recommendation is traced back to official Samsung SIIS documentation and validated against the authoritative deeplink catalog before reaching the user.

**Core principle:** *AI proposes → ANCHOR verifies → Only proven actions reach the response.*

## Problem

Current troubleshooting systems suffer from:

- **Hallucinated actions** — AI models suggest steps not grounded in official documentation
- **Unverified deeplinks** — Arbitrary or fabricated settings URIs that could lead users to wrong device screens
- **Direction mismatches** — Suggesting "Enable Wi-Fi" when the user asked to disable it
- **No provenance** — Users cannot trace a recommendation back to its source evidence

## Solution

ANCHOR introduces a **deterministic verification layer** between AI intelligence and user-facing responses:

1. **Parse** the user's troubleshooting query to extract intent, affected feature, and direction
2. **Analyze** the official SIIS knowledge document to identify relevant troubleshooting sections
3. **Extract** grounded candidate actions strictly from SIIS evidence (no hallucinated steps)
4. **Verify** each candidate against the official Samsung deeplink catalog (578 masked URIs)
5. **Validate** directional consistency (ON/OFF alignment across query, action, and deeplink)
6. **Enforce** official schema compliance on every response

## Core Innovation

### Proof-Carrying Architecture

Unlike conventional RAG systems that retrieve and generate, ANCHOR **proves** its outputs:

- Every action traces to a specific SIIS section with verbatim evidence
- Every deeplink resolves to an exact catalog entry (or `bixby://dummy_positive` for settings navigation)
- Every direction is validated across query → action → deeplink
- External URLs are categorically rejected — only `bixby://masked/*` URIs pass through
- The official `ContextDeeplinkResponse` schema is enforced on every response

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Vue 3 Frontend                           │
│  User Query → Evidence Graph → Action Card → Deeplink Card      │
│                   (Frozen Visual Design)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │ /api/diagnose
┌────────────────────────▼────────────────────────────────────────┐
│                    FastAPI Backend (Port 8000)                   │
│                                                                 │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │ anchor_ai    │→ │ Maitri Verifier  │→ │ Deeplink         │  │
│  │ Intelligence │  │ (student_kit/    │  │ Validator        │  │
│  │ Engine       │  │  verification.py)│  │                  │  │
│  └──────────────┘  └──────────────────┘  └──────────────────┘  │
│         ↓                   ↓                     ↓            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │        Schema Validator (student_kit/schema.py)          │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

## Processing Pipeline

### Stage 1: Query Understanding (`anchor_ai/query_parser.py`)
- Extracts intent summary, affected feature, user state, and direction (ON/OFF/null)
- Identifies device model and technical keywords
- Decomposes multi-clause queries into individual symptom clauses

### Stage 2: SIIS Parsing (`anchor_ai/siis_parser.py`)
- Parses raw SIIS markdown into structured AST of sections and steps
- Preserves hierarchical section relationships
- Identifies actionable vs. diagnostic sections

### Stage 3: Relevance Filtering (`anchor_ai/relevance_engine.py`)
- Multi-stage relevance scoring to isolate pertinent sections
- Prunes noise sections unrelated to the user's specific symptoms

### Stage 4: Action Extraction (`anchor_ai/action_extractor.py`)
- Extracts candidate actions strictly grounded in SIIS evidence text
- Each candidate carries explicit provenance metadata
- Optional LLM semantic refinement (Gemini) with deterministic fallback

### Stage 5: Verification (`student_kit/verification.py`)
- Matches candidates against 578-entry deeplink catalog
- Validates ON/OFF direction consistency across query, action, and deeplink type
- Rejects actions with no catalog match (unless eligible for `bixby://dummy_positive` settings fallback)

### Stage 6: Deeplink Safety (`backend/validators/deeplink_validator.py`)
- Strips any external URL (http/https/ftp/www) from responses
- Re-validates all deeplinks against the authoritative catalog
- Enforces direction alignment at the response level

### Stage 7: Schema Validation (`backend/services/schema_validator.py`)
- Final round-trip validation against official `ContextDeeplinkResponse` Pydantic schema
- Rejects any response that fails schema compliance

## Evidence Grounding

All ANCHOR actions are grounded in the official Samsung SIIS (Samsung Internal Information System) knowledge store:

- **20 official SIIS response documents** covering Galaxy device troubleshooting scenarios
- Evidence text is extracted verbatim from SIIS content — never generated
- Each candidate action carries `evidence_text` traced to its source section

## Direction-Aware Deeplink Resolution

ANCHOR enforces strict directional consistency:

| Query Direction | Action Direction | Deeplink Type | Result |
|---|---|---|---|
| "Turn OFF Wi-Fi" | Disable Wi-Fi | `offURL` | ✓ PASS |
| "Turn OFF Wi-Fi" | Enable Wi-Fi | `onURL` | ✗ REJECTED |
| "Turn ON Bluetooth" | Enable Bluetooth | `onURL` | ✓ PASS |
| "Turn ON Bluetooth" | Disable Bluetooth | `offURL` | ✗ REJECTED |

## Verification Layer

The verification layer (`student_kit/verification.py`) applies these checks:

1. **Evidence grounding** — Candidate evidence must exist in the SIIS response
2. **Catalog matching** — Action text must match a catalog entry's description/message
3. **Direction validation** — No query↔action or action↔deeplink direction contradictions
4. **Disambiguation** — Multiple catalog matches require manual disambiguation (rejected)
5. **Fallback** — SIIS-grounded settings navigation steps use `bixby://dummy_positive`

## API Specification

### `GET /health`
Health check endpoint.

**Response:** `{"status": "ok"}`

### `POST /v1/troubleshoot`
Official Theme 2 troubleshooting endpoint.

**Request:**
```json
{
  "query": "My Galaxy A17 screen looks distorted right after I received the phone.",
  "siis_response": {
    "title": "Screen does not rotate on Galaxy phone or tablet",
    "content": "## Screen Rotation Troubleshooting\nIf your device's screen is not rotating..."
  },
  "row_id": "row_20"
}
```

**Response:** `ContextDeeplinkResponse` (official schema from `student_kit/schema.py`)

```json
{
  "contexts": [
    {
      "goal": "Troubleshoot Display & Device Settings issue",
      "title": "Screen does not rotate on Galaxy phone or tablet",
      "score": 1.0,
      "actions": [
        {
          "actionName": "Adjust Screen Orientation Settings",
          "description": "It will open the Adjust settings screen",
          "stepGroups": [
            {
              "steps": [
                "Using two fingers, swipe down from the top of the screen to open the Quick settings panel.",
                "Locate the screen orientation icon."
              ],
              "actionableDeeplink": {
                "deeplink": "bixby://dummy_positive",
                "description": "It will open the Adjust settings screen",
                "message": "Open the Adjust device settings screen"
              },
              "validationDeeplink": null
            }
          ],
          "category": "auto"
        }
      ]
    }
  ]
}
```

### `POST /api/diagnose`
Dashboard endpoint for the Vue 3 frontend. Accepts `{ "query": "..." }` and returns full visual state including evidence graph data, pipeline stages, and validation status.

## Local Setup

### Prerequisites
- Python 3.10+ (tested with 3.13)
- Node.js 18+ and npm
- No API keys required (deterministic mode by default)
- Optional: `GEMINI_API_KEY` environment variable for LLM semantic refinement

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI backend
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

The backend will:
- Pre-load the deeplink catalog (578 entries) and SIIS responses (20 documents) into memory
- Initialize the IntelligenceEngine and ActionVerifier
- Serve the API on `http://localhost:8000`

### Frontend Setup

```bash
# Install Node dependencies
npm install

# Start Vite dev server (proxies /api to localhost:8000)
npm run dev
```

The frontend runs on `http://localhost:5173` with Vite HMR and proxies all `/api/*` requests to the FastAPI backend.

### Production Build

```bash
npm run build
```

Outputs optimized assets to `dist/`.

## Testing

### Python Tests (43 tests)

```bash
python3 -m pytest tests/ backend/tests/ -v
```

Covers:
- `anchor_ai` intelligence layer (query parsing, SIIS parsing, action extraction, relevance filtering)
- Verification layer (evidence grounding, catalog matching, direction validation)
- FastAPI backend (endpoint behavior, error handling, schema validation, cache behavior)
- Deeplink safety (URL rejection, direction mismatch filtering)

### Frontend Build

```bash
npm run build
```

Verifies all 37 modules compile cleanly with 0 warnings.

## Evaluation

### Benchmark (20 official SIIS rows)

```bash
python3 -m benchmark.run_benchmark
```

**Measured results (deterministic mode, no LLM):**

| Metric | Value |
|---|---|
| Total Queries | 20 |
| Schema-Valid Responses | 20 (100%) |
| Candidate Actions Proposed | 139 |
| Verified Actions Approved | 86 |
| Rejected Actions Filtered | 53 |
| Resolved Catalog Deeplinks | 86 |
| Direction Mismatches | 0 |
| External URL Leakages | 0 |
| Average Pipeline Latency | 6.4 ms |

### Results File

```bash
python3 benchmark/generate_results.py
```

Generates `results.jsonl` — one JSON-Lines entry per SIIS row with the full `ContextDeeplinkResponse`.

## Project Structure

```
ANCHOR/
├── backend/                    # FastAPI backend
│   ├── api/                    # Route handlers (health, troubleshoot, dashboard)
│   ├── cache/                  # In-memory singleton cache for catalogs/engines
│   ├── models/                 # Pydantic request/response/internal models
│   ├── pipeline/               # Orchestrator connecting all components
│   ├── services/               # Intelligence, verification, schema services
│   ├── validators/             # Request and deeplink safety validators
│   └── tests/                  # Backend integration tests (21 tests)
├── anchor_ai/                  # Intelligence layer (query→action extraction)
│   ├── engine.py               # IntelligenceEngine orchestrator
│   ├── query_parser.py         # Intent/direction/device extraction
│   ├── siis_parser.py          # SIIS markdown → structured AST
│   ├── relevance_engine.py     # Multi-stage relevance filtering
│   ├── action_extractor.py     # Grounded candidate action extraction
│   ├── llm_client.py           # Optional Gemini LLM client (graceful fallback)
│   └── models.py               # Intelligence layer data models
├── student_kit/                # Official Samsung Student Kit data
│   ├── schema.py               # Official ContextDeeplinkResponse Pydantic schema
│   ├── verification.py         # ActionVerifier (catalog matching + direction validation)
│   ├── deeplinks.json          # 578 masked Samsung Bixby deeplinks
│   ├── siis_responses.json     # 20 official SIIS knowledge documents
│   ├── input.txt               # 20 official benchmark queries
│   └── sample_output.json      # Official Theme 2 reference response
├── benchmark/                  # Evaluation framework
│   ├── run_benchmark.py        # 20-row SIIS benchmark runner
│   ├── generate_results.py     # results.jsonl generator
│   └── metrics.py              # Benchmark metric models
├── tests/                      # anchor_ai unit tests (22 tests)
├── src/                        # Vue 3 frontend
│   ├── App.vue                 # Main application
│   ├── components/             # 12 UI components
│   └── index.css               # Global styles
├── results.jsonl               # Pipeline output for all 20 SIIS queries
├── requirements.txt            # Python dependencies
├── package.json                # Node dependencies
├── vite.config.js              # Vite config with API proxy
└── index.html                  # Frontend entry point
```

## Known Limitations

1. **LLM dependency is optional** — Without a Gemini API key, the engine runs in fully deterministic mode using rule-based extraction. This produces correct but potentially less nuanced action names.
2. **Dummy positive fallback** — When a grounded SIIS settings step has no exact catalog deeplink match, the system uses `bixby://dummy_positive` as a navigation placeholder. This is functionally correct but does not deep-link to the exact settings screen.
3. **No real-time SIIS retrieval** — The pipeline requires the SIIS response to be provided as input (per Theme 2 specification). It does not perform live SIIS document retrieval.
4. **Candidate volume** — Some complex SIIS documents produce many candidate actions (up to 32 per row). The verification layer correctly filters these, but the response may contain more actions than necessary for simple queries.
5. **Evaluation dataset coverage** — The 20 official SIIS rows cover screen-related troubleshooting scenarios. Performance on non-screen categories has not been benchmarked.

## Team

**Team ANCHOR** — Samsung PRISM Generative AI Hackathon 3.0

1. Vedaang Pratap Singh
2. Mayank Singh
3. Maitri Tyagi
4. Aryaman Narain Pandey