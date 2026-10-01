# ⚓ ANCHOR: Proof-Carrying Guided Troubleshooting Engine

[![Samsung PRISM GenAI Hackathon 3rd Edition](https://img.shields.io/badge/Samsung%20PRISM-GenAI%20Hackathon%203rd%20Edition-blue?style=for-the-badge)](https://github.com/AryamanPandey-art/ANCHOR)
[![Theme](https://img.shields.io/badge/Theme%2002-Smart%20Guided%20Troubleshooting-8A2BE2?style=for-the-badge)](#-theme-overview)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Vue 3](https://img.shields.io/badge/Frontend-Vue%203%20%2B%20Vite-4FC08D?style=for-the-badge&logo=vue.js)](https://vuejs.org)
[![Tests](https://img.shields.io/badge/Tests-50%2F50%20Passed-success?style=for-the-badge)](https://pytest.org)
[![Release Tag](https://img.shields.io/badge/Tag-PRISM__GENAI__HACKATHON__Y2026-orange?style=for-the-badge)](#-submission-metadata)

> **ANCHOR** is an end-to-end, deterministic, proof-carrying troubleshooting engine designed for Samsung Galaxy devices. It converts ambiguous natural-language customer complaints into ordered, evidence-grounded troubleshooting steps and resolves them to verified Samsung Settings deep links — with a 0% hallucination guarantee.

---

## 📋 Table of Contents
- [Executive Summary](#-executive-summary)
- [Theme Overview](#-theme-overview)
- [System Architecture & Pipeline](#-system-architecture--pipeline)
- [Core Innovations & Guardrails](#-core-innovations--guardrails)
- [Repository Structure](#-repository-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup (FastAPI)](#backend-setup-fastapi)
  - [Frontend Setup (Vue 3 + Vite)](#frontend-setup-vue-3--vite)
- [API Reference](#-api-reference)
- [Benchmarking & Evaluation](#-benchmarking--evaluation)
- [Testing](#-testing)
- [Hackathon Submission Checklist](#-hackathon-submission-checklist)
- [Team Information](#-team-information)

---

## 🎯 Executive Summary

Modern device troubleshooting frequently suffers from three fundamental bottlenecks:
1. **Hallucination Risk**: Generic LLMs invent non-existent settings, inaccurate menu paths, or invalid actions.
2. **Direction Inversion**: Models confuse "Turn On" and "Turn Off" operations (e.g. enabling airplane mode vs disabling it).
3. **Actionability Gap**: Standard support articles leave users navigating multi-level menus manually without direct deep link execution.

**ANCHOR** solves this by adopting a **"LLM Proposes, Deterministic Gate Disposes"** architecture. No troubleshooting step reaches the user unless it is grounded in provided Samsung SIIS evidence, direction-verified, matched against an official 578-entry masked deep link catalog, and schema-validated.

---

## 🏷 Theme Overview

* **Theme ID**: `Theme 02 — Smart Guided Troubleshooting Engine`
* **Samsung's Target**: Structured REST API, reusable deep link mapping, robust evidence grounding, fast-path caching, zero raw URL leakage.
* **Our Solution**: A two-tier hybrid intelligence pipeline combining structured natural language intent parsing with deterministic verification algorithms, Pydantic v2 schema enforcement, and a real-time diagnostic dashboard.

---

## 🏗 System Architecture & Pipeline

```
                                  USER QUERY
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │    Query & Intent Parser   │
                        │ (Direction & State Matrix)│
                        └─────────────┬─────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │   SIIS Evidence Parser    │
                        │ (Sentence-level Grounding)│
                        └─────────────┬─────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │   Intelligence Engine     │
                        │  (Candidate Generation)   │
                        └─────────────┬─────────────┘
                                      │
                        ══════════════╪══════════════  [DETERMINISTIC GATE]
                                      ▼
                        ┌───────────────────────────┐
                        │  Deterministic Verifier   │
                        │  • SIIS Grounding Check   │
                        │  • Direction Safety Match │
                        └─────────────┬─────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │  Deep Link Resolver       │
                        │  • 578-entry Masked Map   │
                        │  • Strict bixby:// URI    │
                        │  • Zero URL Leakage Guard │
                        └─────────────┬─────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │ Fast-Path Memory Cache    │
                        │  (Sub-15ms Latency Path)  │
                        └─────────────┬─────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │  Official Schema Validator│
                        │ (ContextDeeplinkResponse) │
                        └─────────────┬─────────────┘
                                      │
                                      ▼
                         STRUCTURED JSON RESPONSE
```

---

## 🛡 Core Innovations & Guardrails

| Feature | Description | Benefit |
|---|---|---|
| **Deterministic Grounding Gate** | Re-verifies every candidate action against SIIS source text using exact and fuzzy semantic overlap. | Eliminates LLM hallucinations. |
| **Direction & State Safety** | Distinguishes opposing actions (Enable vs. Disable, Turn On vs. Turn Off, Connect vs. Disconnect). | Prevents destructive or reversed device operations. |
| **Masked Deep Link Catalog** | Matches verified settings to sanitized `bixby://masked/act/<hash>` identifiers across 578 catalogued actions. | Guarantees instant single-tap navigation with zero HTTP URL leakage. |
| **Sub-15ms Fast Path Cache** | In-memory tokenized LRU cache for high-frequency queries and repeated symptom patterns. | Ultra-low latency and reduced compute footprint. |
| **100% Contract Compliance** | Validated against official Samsung `student_kit.schema.ContextDeeplinkResponse`. | Seamless drop-in evaluation readiness. |

---

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

## Context-Safe Cache Architecture (A3 Compliance)

ANCHOR implements a deterministic, multi-tiered response cache constrained by troubleshooting context boundaries:

- **Exact Cache Key**: `SHA256(SIIS_Title + SIIS_Content) + Normalized_Query`
- **Semantic Paraphrase Key**: `SHA256(SIIS_Title + SIIS_Content) + Direction (ON / OFF / null)`
- **Safety Guarantees**:
  - **SIIS Isolation**: One SIIS article never returns cached responses from another article.
  - **Direction Isolation**: `ON` requests never return `OFF` cached actions and vice versa.
  - **Zero Contamination**: Responses are cached only after strict deterministic schema validation.

### Decision Engine Semantics

| Decision Status | Meaning | Response Representation |
|---|---|---|
| **PASS** | AI proposed actions verified & grounded against SIIS and Deeplink Catalog | Non-empty Goal with verified actions & deeplinks |
| **REJECTED (SAFE)** | Decision engine intentionally blocked unsupported actions (e.g., physical damage, direction mismatch) | Schema-valid response with `contexts: []` |
| **ERROR** | Unhandled system or parsing exception | HTTP 422 or 500 status |


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

### Python Tests (50 tests)

```bash
python3 -m pytest tests/ backend/tests/ -v
```

Covers:
- `anchor_ai` intelligence layer (query parsing, SIIS parsing, action extraction, relevance filtering)
- Verification layer (evidence grounding, catalog matching, direction validation)
- FastAPI backend (health check, endpoint behavior, error handling, schema validation)
- Context-safe caching (exact repeat hit, semantic paraphrase hit, SIIS isolation, ON vs OFF isolation)
- Deeplink safety (external URL rejection, direction mismatch rejection, water damage rejection)

### Frontend Build

```bash
npm run build
```

Verifies all 37 modules compile cleanly with 0 warnings.

## Evaluation & Official Benchmark (A1–A5)

### Benchmark Execution

```bash
python3 benchmark/run_benchmark.py
```

### Measured Benchmark Results

| Evaluation Metric | Measured Result | Hackathon Target | Status |
|---|---|---|---|
| **A1 Schema Validity** | **100.0%** (20/20 rows) | $\ge 90\%$ | **PASS** |
| **A2 Deeplink Resolution** | **86 Resolved** / 0 Invalid | Valid Catalog/Fallback | **PASS** |
| **A2 Direction Consistency** | **0 Mismatches** | 0 Mismatches | **PASS** |
| **A2 URL Safety** | **0 External URL Leaks** | 0 Leaks | **PASS** |
| **A3 Cold Latency (p95)** | **16.95 ms** | $\le 8000\text{ ms}$ | **PASS** |
| **A3 Repeat Hit Rate** | **100.0%** (20/20) | $\ge 90\%$ | **PASS** |
| **A3 Repeat Latency (p95)** | **0.054 ms** | $\le 300\text{ ms}$ | **PASS** |
| **A3 Paraphrase Hit Rate** | **100.0%** (160/160) | $\ge 80\%$ | **PASS** |
| **A3 Paraphrase Latency (p95)** | **0.038 ms** | Sub-millisecond | **PASS** |
| **A5 Query Variations** | **160 Natural Variations** (8/row) | 8–10 per row | **PASS** |

### Results Generation

```bash
python3 benchmark/generate_results.py
```

Generates `results.jsonl` — 20 rows matching the exact required schema with 8 unique natural language paraphrases per query and official `ContextDeeplinkResponse` payload.

## 📁 Repository Structure

```
ANCHOR/
├── backend/                        # High-performance FastAPI backend service
│   ├── main.py                     # Application entrypoint & global middleware
│   ├── api/                        # API route controllers (/health, /v1/troubleshoot)
│   ├── cache/                      # In-memory LRU cache & singleton loaders
│   ├── models/                     # Request, internal, catalog & error Pydantic models
│   ├── pipeline/                   # Pipeline orchestrator & step executors
│   ├── services/                   # Intelligence service & schema validators
│   ├── validators/                 # Request sanitizer & deep link direction guard
│   └── tests/                      # Unit & integration test suite (28 scenarios)
├── anchor_ai/                      # Core intelligence & NLP layer
│   ├── intelligence_engine.py      # Candidate action extraction engine
│   ├── query_parser.py             # User complaint intent & state parser
│   ├── siis_parser.py              # Samsung SIIS evidence processor
│   ├── relevance_engine.py         # Semantic relevance ranker
│   └── action_verifier.py          # Deterministic contract verifier
├── benchmark/                      # Evaluation & benchmarking suite
│   ├── run_benchmark.py            # 20-row dataset evaluation runner
│   ├── metrics.py                  # Evaluation metrics & summary aggregators
│   └── generate_results.py         # Results.jsonl generator
├── src/                            # Modern Vue 3 + Vite interactive UI
│   ├── App.vue                     # Main interactive application
│   ├── components/                 # Diagnostics visualizer, chat & telemetry components
│   └── assets/                     # Styles, typography, and iconography
├── Submission Content/             # Official Hackathon Assets
│   ├── Anchor-Demo.mp4             # 5-minute Product Walkthrough Video
│   └── SRMIST_ANCHOR_Submission.pptx # Hackathon Presentation Deck
├── student_kit/                    # Official Samsung PRISM evaluation schemas & contracts
├── participant-kit/                # Participant evaluation toolkit & runner
├── tests/                          # Root test suite (anchor_ai modules)
├── package.json                    # Frontend dependencies & scripts
├── vite.config.js                  # Vite bundler configuration
└── README.md                       # Master documentation
```

---

## 📑 Hackathon Submission Checklist

- [x] **Source Code**: Fully modularized and documented (`backend/`, `anchor_ai/`, `src/`).
- [x] **Presentation**: `Submission Content/SRMIST_ANCHOR_Submission.pptx`.
- [x] **Demo Video**: `Submission Content/Anchor-Demo.mp4` (Product walkthrough demonstration).
- [x] **AI Disclosure**: Transparently documented hybrid LLM + deterministic verification layer (`AI_DISCLOSURE.md`).
- [x] **README**: Complete reproducible installation, API contracts, and evaluation guide.
- [x] **Release Tag**: `PRISM_GENAI_HACKATHON_Y2026`.

---

## 👥 Team Information

* **Team Name**: `ANCHOR`
* **Institution**: SRM Institute of Science and Technology (SRMIST)
* **Hackathon**: Samsung PRISM Generative AI Hackathon — 3rd Edition (2026–27)

### Team Members:
1. **Vedaang Pratap Singh**
2. **Mayank Singh**
3. **Maitri Tyagi**
4. **Aryaman Narain Pandey**

---

<div align="center">
  <sub>Organised by the Language AI Team and the PRISM Team, Samsung R&D Institute India</sub>
</div>