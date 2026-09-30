# ANCHOR — AI Disclosure Document

**Samsung PRISM Generative AI Hackathon 3.0 — Theme 2**
**Team:** Team ANCHOR (Vedaang Pratap Singh, Mayank Singh, Maitri Tyagi, Aryaman Narain Pandey)
**Date:** September 30, 2026

---

## 1. AI / GenAI Usage Declaration

ANCHOR uses Generative AI as an **optional semantic refinement layer** within a deterministic, proof-carrying troubleshooting architecture. The system is designed to function correctly with or without an LLM.

### Where GenAI / LLMs Are Used

| Component | GenAI Role | Deterministic Alternative |
|---|---|---|
| `anchor_ai/llm_client.py` | **Optional** — Gemini 2.5 Flash for semantic refinement of candidate action names and descriptions extracted from SIIS | Fully deterministic rule-based extraction (`anchor_ai/action_extractor.py`) runs as baseline and fallback |
| Query Parsing | Not used | Deterministic regex + keyword parser (`anchor_ai/query_parser.py`) |
| SIIS Parsing | Not used | Deterministic markdown AST parser (`anchor_ai/siis_parser.py`) |
| Verification | Not used | Deterministic catalog matching + direction validation (`student_kit/verification.py`) |
| Deeplink Resolution | Not used | Deterministic catalog lookup (`backend/validators/deeplink_validator.py`) |
| Schema Validation | Not used | Deterministic Pydantic validation (`backend/services/schema_validator.py`) |

**Important:** The LLM is disabled by default (`enable_llm=False`). When no `GEMINI_API_KEY` is set, the engine uses 100% deterministic processing. All 43 tests pass and all 20 benchmark queries produce schema-valid responses without any LLM.

### What the Model Proposes

When enabled, the LLM receives:
- The user's troubleshooting query
- The SIIS document title
- Relevant SIIS section texts (already filtered by the deterministic relevance engine)

The LLM is asked to refine candidate action names and provide structured interpretation. Its output is treated as **advisory only** — it cannot introduce actions not grounded in SIIS evidence, and it cannot bypass the verification layer.

### What Is Deterministic (Not AI-Generated)

The following are **entirely deterministic** and contain zero AI-generated content:

1. **Query intent extraction** — Direction (ON/OFF), feature, state, device model
2. **SIIS document parsing** — Structured AST with sections and steps
3. **Relevance filtering** — Multi-stage keyword/semantic scoring
4. **Evidence grounding** — Verbatim text provenance from SIIS
5. **Catalog matching** — Exact match against 578 masked Samsung deeplinks
6. **Direction validation** — ON/OFF consistency across query → action → deeplink type
7. **URL safety enforcement** — Rejection of all http/https/ftp/www URIs
8. **Schema validation** — Pydantic ContextDeeplinkResponse enforcement
9. **Pipeline orchestration** — FastAPI request/response handling

## 2. Sources of Truth

| Data Source | Origin | Modification |
|---|---|---|
| `student_kit/siis_responses.json` | Official Samsung Student Kit | **Unmodified** — 20 SIIS documents |
| `student_kit/deeplinks.json` | Official Samsung Student Kit | **Unmodified** — 578 masked deeplinks |
| `student_kit/schema.py` | Official Samsung Student Kit | **Unmodified** — Pydantic schema |
| `student_kit/input.txt` | Official Samsung Student Kit | **Unmodified** — 20 benchmark queries |
| `student_kit/sample_output.json` | Official Samsung Student Kit | **Unmodified** — Reference response |

ANCHOR treats these files as **immutable authoritative data**. No official Samsung data has been modified, augmented, or regenerated.

## 3. Verification Architecture

ANCHOR's core innovation is that **no AI-proposed action can reach the user without passing deterministic verification**:

```
AI Proposes → ANCHOR Verifies → Only Verified Actions Reach Response
```

Verification checks:
1. Evidence text exists verbatim in the SIIS response
2. Action matches a catalog entry by description/message text
3. Direction alignment: query ↔ action ↔ deeplink type (ON/OFF)
4. Deeplink URI exists in the official 578-entry catalog
5. No external URLs (http/https) pass through
6. Response passes official Pydantic schema validation

**Any check failure results in the action being filtered out of the response.** The system never claims a verified action when verification has failed.

## 4. Human / Team Involvement

| Contribution | Who |
|---|---|
| System architecture design | Team ANCHOR (human) |
| Pipeline orchestrator implementation | Team ANCHOR (human) |
| Intelligence engine design | Team ANCHOR (human) |
| Verification layer logic | Team ANCHOR (human) |
| Vue 3 frontend design and implementation | Team ANCHOR (human) |
| Test suite authoring | Team ANCHOR (human) |
| Benchmark framework | Team ANCHOR (human) |
| Code implementation assistance | AI pair programming tools were used to accelerate development |

## 5. Limitations and Honest Assessment

1. **Deterministic mode produces functional but basic action names** — Without LLM refinement, action names are extracted mechanically from SIIS section headings.
2. **Dummy positive fallback** — Settings navigation steps that are clearly grounded in SIIS but have no exact catalog match use `bixby://dummy_positive`. This is functionally correct but is a placeholder, not a precise deeplink.
3. **No live SIIS retrieval** — SIIS responses are provided as input per the Theme 2 specification.
4. **Coverage limited to provided SIIS data** — The system can only troubleshoot scenarios covered by the 20 official SIIS documents.

## 6. AI-Generated vs. Deterministic Content in Responses

| Response Field | Source |
|---|---|
| `contexts[].goal` | Deterministic — from query intent + SIIS title |
| `contexts[].title` | Deterministic — from SIIS document title |
| `contexts[].score` | Deterministic — candidate confidence average |
| `actions[].actionName` | Deterministic baseline, optionally LLM-refined |
| `actions[].description` | Deterministic — from catalog match or SIIS section |
| `stepGroups[].steps` | Deterministic — verbatim from SIIS evidence |
| `actionableDeeplink` | Deterministic — exact catalog entry or dummy_positive |
| `validationDeeplink` | Deterministic — exact catalog validation entry |

---

*This disclosure accurately represents ANCHOR's AI usage as of the submission date. The system is designed to be transparent about what is AI-generated versus deterministically verified.*
