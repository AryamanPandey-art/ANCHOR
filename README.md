# ⚓ ANCHOR: Proof-Carrying Guided Troubleshooting Engine

[![Samsung PRISM GenAI Hackathon 3rd Edition](https://img.shields.io/badge/Samsung%20PRISM-GenAI%20Hackathon%203rd%20Edition-blue?style=for-the-badge)](https://github.com/AryamanPandey-art/ANCHOR)
[![Theme](https://img.shields.io/badge/Theme%2002-Smart%20Guided%20Troubleshooting-8A2BE2?style=for-the-badge)](#-theme-overview)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Vue 3](https://img.shields.io/badge/Frontend-Vue%203%20%2B%20Vite-4FC08D?style=for-the-badge&logo=vue.js)](https://vuejs.org)
[![Tests](https://img.shields.io/badge/Tests-41%2F41%20Passed-success?style=for-the-badge)](https://pytest.org)
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
│   └── tests/                      # Unit & integration test suite (21 scenarios)
├── anchor_ai/                      # Core intelligence & NLP layer
│   ├── intelligence_engine.py      # Candidate action extraction engine
│   ├── query_parser.py             # User complaint intent & state parser
│   ├── siis_parser.py              # Samsung SIIS evidence processor
│   ├── relevance_engine.py         # Semantic relevance ranker
│   └── action_verifier.py          # Deterministic contract verifier
├── benchmark/                      # Evaluation & benchmarking suite
│   ├── run_benchmark.py            # 20-row dataset evaluation runner
│   ├── metrics.py                  # Evaluation metrics & summary aggregators
│   └── compare.py                  # Regression comparator
├── src/                            # Modern Vue 3 + Vite interactive UI
│   ├── App.vue                     # Main interactive application
│   ├── components/                 # Diagnostics visualizer, chat & telemetry components
│   └── assets/                     # Styles, typography, and iconography
├── server/                         # Express / Node middleware runner
├── student_kit/                    # Official Samsung PRISM evaluation schemas & contracts
├── participant-kit/                # Participant evaluation toolkit & runner
├── tests/                          # Root test suite (anchor_ai modules)
├── package.json                    # Frontend dependencies & scripts
├── vite.config.js                  # Vite bundler configuration
└── README.md                       # Master documentation
```

---

## 🚀 Getting Started

### Prerequisites
- **Python**: Version `3.10`, `3.11`, or `3.12` (Python 3.14 compatible)
- **Node.js**: Version `18.0+`
- **npm** or **yarn**

---

### Backend Setup (FastAPI)

1. **Navigate to the repository root**:
   ```bash
   cd ANCHOR
   ```

2. **Install Python dependencies**:
   ```bash
   pip install fastapi uvicorn pydantic pytest lxml python-pptx
   ```

3. **Start the FastAPI Backend**:
   ```bash
   python -m backend.main
   ```
   *The backend will start at `http://localhost:8000`.*
   *Interactive Swagger API documentation available at `http://localhost:8000/docs`.*

---

### Frontend Setup (Vue 3 + Vite)

1. **Install Node dependencies**:
   ```bash
   npm install
   ```

2. **Launch the development server**:
   ```bash
   npm run dev
   ```
   *The frontend will launch at `http://localhost:5173`.*

3. **Launch Full-Stack Concurrently**:
   ```bash
   npm start
   ```

---

## 📡 API Reference

### 1. Health Check
* **Endpoint**: `GET /health`
* **Response `200 OK`**:
  ```json
  {
    "status": "ok",
    "version": "1.0.0"
  }
  ```

---

### 2. Guided Troubleshooting Pipeline
* **Endpoint**: `POST /v1/troubleshoot`
* **Request Header**: `Content-Type: application/json`

#### Example Request:
```json
{
  "query": "Turn on Touch Sensitivity because my screen protector is thick",
  "siis_response": {
    "title": "Touchscreen issues on a Galaxy phone or tablet",
    "content": "Increase the screen sensitivity to use it with a screen protector. Navigate to Settings > Display > Touch sensitivity and toggle the switch to turn it on."
  },
  "row_id": "row_001"
}
```

#### Example Response (`200 OK`):
```json
{
  "query": "Turn on Touch Sensitivity because my screen protector is thick",
  "siis_title": "Touchscreen issues on a Galaxy phone or tablet",
  "actions": [
    {
      "step_number": 1,
      "action_name": "Touch sensitivity",
      "direction": "turn_on",
      "grounded": true,
      "deeplink": "bixby://masked/act/1b0d34e9b4",
      "target_setting": "Display > Touch sensitivity"
    }
  ],
  "is_grounded": true,
  "confidence_score": 0.98,
  "metadata": {
    "cached": false,
    "execution_time_ms": 12.4
  }
}
```

---

## 📊 Benchmarking & Evaluation

Run the automated evaluation benchmark across the standard 20-row SIIS dataset:

```bash
python -m benchmark.run_benchmark
```

### Key Performance Metrics:
* **Schema Validity**: `100.0%`
* **SIIS Grounding Precision**: `100.0%`
* **Direction Inversion Rate**: `0.0%`
* **Raw URL Leakage**: `0 instances`
* **Average Latency (Cold)**: `< 45ms`
* **Average Latency (Cached)**: `< 12ms`

---

## 🧪 Testing

The repository includes a comprehensive 41-scenario test suite covering query normalization, SIIS parsing, candidate extraction, direction verification, schema validation, and API edge cases.

Execute all tests with `pytest`:
```bash
python -m pytest
```

Output:
```text
backend/tests/test_backend.py ..................... [ 51%]
tests/test_action_extractor.py ...                  [ 58%]
tests/test_intelligence_engine.py .                 [ 60%]
tests/test_query_parser.py ......                   [ 75%]
tests/test_relevance_engine.py ..                   [ 80%]
tests/test_siis_parser.py ...                       [ 87%]
tests/test_verification.py .....                    [100%]

======================= 41 passed in 1.36s =======================
```

---

## 📑 Hackathon Submission Checklist

- [x] **Source Code**: Fully modularized and documented (`backend/`, `anchor_ai/`, `src/`).
- [x] **Presentation**: `SRMIST_ANCHOR_Submission.pptx` & `SRMIST_ANCHOR_Submission.pdf`.
- [x] **Demo Video**: Max 5-minute product walkthrough demonstration.
- [x] **AI Disclosure**: Transparently documented hybrid LLM + deterministic verification layer.
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