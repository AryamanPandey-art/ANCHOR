# ANCHOR

### Proof-Carrying Troubleshooting Engine

ANCHOR is a deterministic troubleshooting and verification engine designed to provide **grounded, evidence-backed device troubleshooting actions** using the official Samsung Student Kit dataset.

Instead of allowing an AI system to freely generate troubleshooting actions or deeplinks, ANCHOR constructs a verifiable chain:

**User Query → Intent → Official Evidence → Proposed Action → Official Deeplink → Contract Guard → Verified Result**

Every automated action must satisfy explicit grounding, support, direction, deeplink, and safety constraints before it can be presented as executable.

---

## Overview

Modern troubleshooting systems can produce plausible-looking actions that are unsupported by the underlying documentation or point to invalid application routes.

ANCHOR addresses this problem through a **proof-carrying troubleshooting pipeline**.

The system:

1. Parses the user's troubleshooting request.
2. Determines the relevant troubleshooting intent and requested direction.
3. Retrieves matching evidence from the official Samsung Student Kit dataset.
4. Extracts an action supported by that evidence.
5. Resolves the proposed action against the official deeplink catalog.
6. Validates direction consistency.
7. Applies deterministic Contract Guard checks.
8. Produces either a verified `PASS` or a safe `REJECT`.

Unsupported, fabricated, ambiguous, or hardware-dependent actions are prevented from reaching automated execution.

---

# Core Architecture

```text
                         USER QUERY
                             │
                             ▼
                    ┌─────────────────┐
                    │  Intent Parser  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ SIIS Retriever  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Action Compiler │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Deeplink     │
                    │    Resolver     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Contract Guard  │
                    │   7 Gates       │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
                 PASS              REJECT
                    │                 │
                    ▼                 ▼
              Verified Action    Safe Rejection
```

---

# Key Design Principles

## 1. Deterministic Processing

The current troubleshooting pipeline does not rely on an LLM to invent actions or deeplinks.

Intent extraction, evidence retrieval, action compilation, catalog resolution, and contract validation are implemented through deterministic processing, including:

- Regex-based intent extraction
- Keyword/token matching
- Jaccard-style relevance matching
- Explicit evidence grounding
- Catalog-based deeplink resolution
- Deterministic contract validation

This makes the verification path reproducible.

## 2. Evidence Grounding

Actions must be grounded in retrieved SIIS evidence. If sufficient supporting evidence cannot be established, the pipeline rejects the proposed action.

## 3. Official Deeplink Verification

Proposed deeplinks are resolved against the official Student Kit deeplink catalog. Fabricated routes such as `settings://fabricated/toggle` are rejected.

## 4. Direction Safety

ANCHOR distinguishes between `ENABLE`, `DISABLE`, and `NONE`. A deeplink that performs the opposite operation from the user's requested direction is rejected.

## 5. Hardware Action Isolation

Troubleshooting procedures requiring physical interaction—such as force restart, hardware button combinations, physical inspection, or hardware recovery—are isolated from automated deeplink execution.

---

# Contract Guard

The **Contract Guard** is the primary verification boundary of ANCHOR.

It validates the proposed troubleshooting result through seven deterministic checks covering:

- Evidence grounding
- Explicit action support
- Hardware intervention isolation
- Deeplink validity
- Official catalog membership
- Direction consistency
- Response/schema validity

A result is only considered executable when the required validation gates pass.

```text
Evidence
   │
   ├── Grounded?
   ├── Action explicitly supported?
   ├── Hardware intervention?
   ├── Deeplink present?
   ├── Deeplink officially catalogued?
   ├── Direction matches?
   └── Response contract valid?
            │
            ▼
        PASS / REJECT
```

---

# Official Student Kit Integration

ANCHOR uses the Samsung Student Kit data stored under:

```text
server/data/student-kit/
```

The integration includes:

```text
siis_responses.json
deeplinks.json
schema.py
sample_output.json
input.txt
```

The audited dataset contains:

- **20 official SIIS records**
- **20 official evaluation queries**
- **578 official masked deeplink URIs**
- Official Pydantic response schema

The Student Kit data is treated as the source of truth for the troubleshooting pipeline.

---

# Supported Pipeline Outcomes

ANCHOR intentionally does not attempt to automate every troubleshooting request.

The audited official query set produced:

| Result | Count |
|---|---:|
| Verified PASS | 6 |
| Safe REJECT | 14 |
| Total | 20 |

The rejected cases primarily represent troubleshooting scenarios where the official evidence requires hardware intervention or otherwise cannot satisfy the automated execution contract.

This behavior is intentional: **a rejection is preferable to an unsupported automated action.**

---

# Frontend

The frontend is implemented as a dark technical console designed around the troubleshooting pipeline.

### Main Navigation

- Overview
- Diagnose
- Evidence
- Solution
- Engine

### Overview

Provides the complete troubleshooting workspace including the user query, intent, SIIS evidence, evidence graph, proposed action, deeplink, contract validation, pipeline status, evidence proof, and verification status.

### Diagnose

Focuses on the user problem, query input, intent classification, and diagnostic pipeline.

### Evidence

Focuses on official SIIS evidence, provenance, grounding, and explicit action support.

### Solution

Focuses on proposed action, action conditions, deeplink resolution, and contract decision.

### Engine

Focuses on Contract Guard, validation gates, decision-engine state, and evidence graph verification.

---

# Evidence Graph

The Evidence Graph visually represents the proof chain:

```text
User Query
     ↓
SIIS Evidence
     ↓
Proposed Action
     ↓
Deeplink
     ↓
Contract Guard
```

The graph responds to the active navigation section:

```text
Diagnose  → Complaint node
Evidence  → SIIS Evidence node
Solution  → Action node
Engine    → Validation node
Overview  → Full graph
```

---

# Safety and Verification Model

ANCHOR follows a **fail-closed** approach. If a required verification condition fails, the result is rejected.

| Test | Result |
|---|---|
| Unsupported action | BLOCKED |
| Fabricated deeplink | BLOCKED |
| Direction mismatch | BLOCKED |
| Missing evidence | BLOCKED |
| Hardware action | BLOCKED |
| Backend exception | BLOCKED |
| Frontend PASS spoof | BLOCKED |
| Empty query | REJECT |

The frontend does not independently grant execution permission. The execution state depends on verified backend contract state.

---

# Validation and Testing

## Automated Test Suite

```text
npm test

57/57 assertions passed
0 failed
0 skipped
```

## Sidebar Navigation Tests

```text
node server/tests/sidebarNav.test.js

37/37 passed
0 failed
```

The navigation test verifies click handling, active state, view switching, header synchronization, and Evidence Graph synchronization.

## Production Build

```bash
npx vite build
```

Result: **SUCCESS — 0 errors, 0 warnings.**

## API Verification

The audited backend was available at:

```text
http://localhost:3001
```

Verified endpoints:

```text
GET  /api/session
GET  /api/data-audit
POST /api/diagnose
```

### Valid Query

```json
{
  "query": "My screen isn't rotating automatically."
}
```

Result: `PASS`

### Empty Query

```json
{
  "query": ""
}
```

Result: `FAIL`

The empty-query gateway issue was fixed so an explicitly supplied empty string is no longer replaced by a default troubleshooting query.

---

# Repository Structure

```text
ANCHOR/
│
├── public/
├── src/
│   ├── components/
│   │   ├── ActionCard.vue
│   │   ├── DeeplinkCard.vue
│   │   ├── EvidenceGraph.vue
│   │   ├── Header.vue
│   │   ├── IntentCard.vue
│   │   ├── PipelineStatusPanel.vue
│   │   ├── ProofVerificationPanel.vue
│   │   ├── SiisEvidenceCard.vue
│   │   ├── UserQueryCard.vue
│   │   └── ValidationCard.vue
│   ├── App.vue
│   └── ...
├── server/
│   ├── engine/
│   │   ├── actionCompiler.js
│   │   ├── contractGuard.js
│   │   ├── deeplinkResolver.js
│   │   ├── intentParser.js
│   │   ├── orchestrator.js
│   │   ├── schemaValidator.js
│   │   └── siisRetriever.js
│   ├── data/
│   │   └── student-kit/
│   │       ├── deeplinks.json
│   │       ├── input.txt
│   │       ├── sample_output.json
│   │       ├── schema.py
│   │       └── siis_responses.json
│   ├── tests/
│   │   ├── pipeline.test.js
│   │   └── sidebarNav.test.js
│   └── index.js
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
├── requirements.txt
└── README.md
```

---

# Technology Stack

### Frontend

- Vue.js
- Vite
- JavaScript
- CSS

### Backend

- Node.js
- Express
- Deterministic troubleshooting engine

### Validation

- Python
- Pydantic
- Official Student Kit `schema.py`

### Testing

- Node.js native test runner
- Integration tests
- Browser/CDP interaction testing

### Version Control

- Git
- GitHub

---

# Local Development

## Prerequisites

- Node.js
- npm
- Python 3.12+
- Pydantic

## Install Dependencies

```bash
npm install
pip install -r requirements.txt
```

## Run the Application

Use the scripts defined in `package.json` for the current repository version.

The audited development environment used:

```text
Frontend: http://localhost:5173/
Backend:  http://localhost:3001/
```

---

# API

## Diagnose

```http
POST /api/diagnose
```

Example:

```json
{
  "query": "My screen isn't rotating automatically."
}
```

The endpoint returns the troubleshooting pipeline result, including evidence, proposed action, deeplink resolution, contract validation, and final verdict.

## Session

```http
GET /api/session
```

Returns current application/session state.

## Data Audit

```http
GET /api/data-audit
```

Provides information about the loaded Student Kit dataset and its records.

---

# Verification Philosophy

ANCHOR is designed around the principle:

> **No evidence, no action.**  
> **No valid contract, no execution.**

The system prioritizes traceability and verification over generating an answer for every possible query.

A successful result should be explainable through a concrete chain of evidence rather than relying solely on model confidence or generated text.

---

# Current Verification Status

The final technical audit reported:

```text
57/57 automated assertions passed
37/37 sidebar navigation assertions passed
Production build passed
Empty-query gateway fix verified
Physical browser interaction verified
Contract Guard adversarial checks passed
Official Student Kit integration verified
```

The final audit classified the implementation as:

**COMPLETE**

with the reported functional, security, gateway, navigation, and browser-interaction checks passing.

---

# Team Contribution Areas

| Area | Responsibility |
|---|---|
| Frontend | Vue interface, visualization, navigation, API integration |
| Backend | Troubleshooting pipeline and API |
| Verification | Contract Guard, deeplink validation, evidence grounding |
| Data Integration | Official Student Kit dataset and schema |
| Testing | Pipeline, navigation, adversarial and browser verification |
| Documentation | Technical audit reports and project documentation |

---

# Project Objective

ANCHOR demonstrates how a troubleshooting system can combine:

**Evidence + deterministic reasoning + catalog verification + contract enforcement + interactive visualization**

to produce troubleshooting results that are traceable and verifiable.

---

## License

This repository contains project-specific implementation code and integrated Samsung Student Kit materials. Refer to the applicable project, competition, and source-material terms before redistributing any third-party dataset or documentation.
