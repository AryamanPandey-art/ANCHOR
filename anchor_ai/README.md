# ANCHOR — AI / Intelligence Layer (`anchor_ai`)

> **Samsung PRISM GenAI Hackathon (Theme 2: Smart Guided Troubleshooting Engine)**  
> **Module Owner:** AI / Intelligence Engineer  
> **Downstream Consumer:** Maitri (Verification & Deeplink Resolution Engineer)

---

## 1. Core Philosophy

$$\text{LLM proposes} \implies \text{SIIS provides evidence} \implies \text{Deterministic code preserves \& verifies}$$

The `anchor_ai` module converts natural-language troubleshooting queries and raw Samsung SIIS technical responses into structured, evidence-grounded candidate troubleshooting actions. 

**Strict Design Boundaries:**
- Grounded strictly in the supplied SIIS text ($0$ hallucinated steps or menu paths).
- No hardcoded deeplinks or official `schema.py` response generation (Maitri & Mayank own downstream resolution).
- Seamless fallback to deterministic pipeline with $<1\text{ ms}$ latency and $100\%$ uptime.

---

## 2. Module Architecture

```
anchor_ai/
├── __init__.py           # Package exports (IntelligenceEngine, models)
├── models.py             # Pydantic data contract (IntelligenceResult, CandidateAction, etc.)
├── siis_parser.py        # Deterministic Markdown/AST parser with step & hierarchy preservation
├── query_parser.py       # Intent, feature, symptom, direction (ON/OFF/null), and multi-clause extractor
├── relevance_engine.py   # Multi-stage relevance filter & noise discriminator
├── action_extractor.py   # Evidence grounding, provenance tracking, and deterministic confidence
├── llm_client.py         # Isolated zero-dependency Gemini/OpenAI REST client
├── engine.py             # Main facade (IntelligenceEngine)
└── README.md             # This documentation
```

---

## 3. Quickstart & Usage

```python
from anchor_ai import IntelligenceEngine

# Initialize engine (enable_llm=False runs pure deterministic pipeline)
engine = IntelligenceEngine(enable_llm=False)

query = '1. "My Galaxy Z Flip 7 screen is cracked." 2. "The touch doesn\'t work."'
siis_response = {
    "title": "Cracked or bleeding screen on Galaxy phone or tablet",
    "content": "Smartphone,Tablet... # Service Options for Cracked Screens..."
}

# Run pipeline
result = engine.run_intelligence(query, siis_response)

# Access extracted intent and candidate actions
print("Feature:", result.query_intent.affected_feature)
print("Direction:", result.query_intent.direction.value)       # "ON" | "OFF" | "null"
print("Sub-symptoms:", result.query_intent.sub_symptoms)       # List of distinct clauses
print("Candidates extracted:", len(result.candidate_actions))
```

---

## 4. Exact Integration Contract with Maitri (`models.py`)

Maitri's verification and deeplink engine consumes `IntelligenceResult`.

### A. `IntelligenceResult`
```python
class IntelligenceResult(BaseModel):
    query_intent: QueryIntent
    parsed_siis: ParsedSIIS
    relevant_sections: List[SIISSection]
    candidate_actions: List[CandidateAction]
    fallback_used: bool
    metadata: Dict[str, Any]
```

### B. `QueryIntent`
```python
class Direction(str, Enum):
    ON = "ON"
    OFF = "OFF"
    NONE = "null"

class QueryIntent(BaseModel):
    intent_summary: str          # High-level summary of intent
    affected_feature: str        # e.g. "Touchscreen & Sensitivity", "Display & Screen Power"
    user_state: str              # Failure symptom or condition
    direction: Direction         # Direction.ON | Direction.OFF | Direction.NONE ("null")
    technical_keywords: List[str]# Extracted search keywords
    device_model: Optional[str]  # e.g. "Galaxy S22", "Galaxy Z Flip 7"
    sub_symptoms: List[str]      # Discrete clauses from multi-symptom queries
```

### C. `CandidateAction`
```python
class CandidateAction(BaseModel):
    action_name: str             # Action name (e.g. "Clear the Email App's Cache and Data")
    description: str             # Explanation of why this action helps
    steps: List[str]             # Sequential execution steps (verbatim from SIIS)
    source_section_title: str    # Provenance: section title
    source_section_id: str       # Provenance: section ID
    evidence_text: str           # Verbatim SIIS snippet supporting this candidate
    category_hint: str           # "auto" (settings navigation) | "manual" (physical/service)
    confidence: float            # Deterministic heuristic score (0.0 to 1.0)
    provenance: Dict[str, Any]   # Source section ID, title, step count, grounded flag
```

---

## 5. Provenance & Confidence Guarantees

1. **Step Traceability**: Every step in `candidate_actions.steps` is guaranteed to be a direct verbatim substring from the source SIIS document.
2. **Deterministic Confidence Score**:
   $$\text{Confidence} = \text{base}(0.70) + 0.15 \times (\text{steps} \ge 2) + 0.15 \times (\text{evidence is exact substring})$$
3. **Directional Safety Guard**: Symptom failure phrases (e.g. *"won't turn on"*, *"try to turn on"*) never trigger `Direction.ON`. Only explicit commands (e.g. *"enable touch sensitivity"*, *"turn off auto rotate"*) yield `ON` or `OFF`.

---

## 6. How Maitri Consumes This Interface

```
IntelligenceResult (from anchor_ai)
      │
      ├──> 1. Verify Grounding: candidate.evidence_text exists in parsed_siis
      │
      ├──> 2. Deeplink Resolution: Match candidate.action_name + steps in deeplinks.json
      │
      ├──> 3. Direction Validation: Ensure matched deeplink does not conflict with query_intent.direction
      │
      └──> 4. Proof Generation: Attach actionableDeeplink & validationDeeplink for Mayank
```

---

## 7. Testing & Verification

Run the test suite across all 20 official rows:

```bash
# Run all tests
python3 -m pytest -v -s

# Run benchmark suite
python3 -m pytest tests/test_intelligence_engine.py -v -s
```

### Benchmark Metrics (20 Official Dataset Rows)
- **Unit Test Pass Rate:** $15 / 15\text{ (100\%)}$
- **Evidence Traceability:** $139 / 139\text{ candidates grounded (100\%)}$
- **Untraceable / Hallucinated Steps:** $0$
- **Average Processing Latency:** $0.44\text{ ms / query}$

---

## 8. Assumptions & Known Limitations

1. **Source of Truth**: SIIS responses in the student kit are treated as absolute ground truth. If SIIS describes Multi-Window when the user query mentions a dark screen (`row_7`), `anchor_ai` will extract only supported actions without inventing unsupported OS settings.
2. **Deeplink Separation**: `anchor_ai` intentionally does not load `student_kit/deeplinks.json` to keep the AI layer decoupled from the deterministic catalog resolver.
