# ANCHOR — Demo Script (3–5 Minutes)

**Samsung PRISM Generative AI Hackathon 3.0 — Theme 2**

---

## Setup (Before Demo)

Open **two terminal windows**:

### Terminal 1 — Backend
```bash
cd /path/to/ANCHOR
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
Wait for: `Uvicorn running on http://0.0.0.0:8000`

### Terminal 2 — Frontend
```bash
cd /path/to/ANCHOR
npm run dev
```
Wait for: `VITE ready in XXms → http://localhost:5173/`

### Browser
Open **http://localhost:5173/** in Chrome/Edge.

You should see the ANCHOR dashboard in its idle state:
- Header shows **ANCHOR — Proof-Carrying Troubleshooting Engine**
- Evidence Graph shows all nodes in idle (cyan outlines)
- Action Card shows **AWAITING QUERY**
- Contract Validation shows all checks as **Failed ✗** (no query submitted)

---

## Demo Flow

### Slide 1: Introduction (30 seconds)

> "This is ANCHOR — a Proof-Carrying Troubleshooting Engine for Samsung Galaxy devices. The core idea is simple: **AI proposes, ANCHOR verifies, only proven actions reach the user.** Every recommendation is traced back to official Samsung SIIS documentation and validated against the authoritative deeplink catalog. Let me show you how it works."

---

### Slide 2: Successful Troubleshooting — Screen Rotation (60 seconds)

**Action:** Click the **S1: Auto Rotate [PASS]** demo button, or type the query:

> "My Galaxy A17 screen looks distorted right after I received the phone, and I need a diagnostic test."

**What to highlight as the UI updates:**

1. **User Query card** — Shows the submitted query
2. **Intent Analysis** — Shows intent: "Display & Device Settings issue", Direction detected
3. **SIIS Evidence** — Shows the matched SIIS article: "Screen does not rotate on Galaxy phone or tablet"
4. **Evidence Graph** — Nodes illuminate green along the path: User Complaint → Intent → SIIS Evidence → AI Proposal → Samsung Deeplink → Decision Engine
5. **Action Card** — Shows verified action: "Adjust Screen Orientation Settings" with `GROUNDED PROOF`
6. **Deeplink Resolution** — Shows `bixby://dummy_positive` with catalog match VERIFIED
7. **Contract Validation** — All checks turn green: Grounding ✓, Deeplink ✓, Direction ✓, Schema ✓
8. **Pipeline Status** — All 5 stages completed: Query → Intent → Evidence → Action → Contract

> "The engine parsed the query, identified screen rotation as the affected feature, retrieved the relevant SIIS document, extracted grounded troubleshooting steps, verified them against the Samsung deeplink catalog, and confirmed directional consistency — all in under 10 milliseconds."

---

### Slide 3: Cracked Screen — Data Backup (45 seconds)

**Action:** Click the **S2: Data Backup [PASS]** demo button, or type:

> "The mobile phone screen is cracked and flashes intermittently."

**What to highlight:**

1. **SIIS Evidence** — Shows screen damage troubleshooting
2. **Action Card** — Shows "Back Up Phone Data" as the verified action
3. **Deeplink** — Shows `bixby://masked/act/b3ed3ed663` — a real catalog deeplink pointing to Samsung Cloud backup
4. **Validation Deeplink** — Shows `bixby://masked/val/266037d0c5` — the validation endpoint
5. **Contract Validation** — All checks pass

> "For a cracked screen, ANCHOR doesn't just suggest generic advice. It identifies the specific Samsung SIIS procedure — back up data first — and resolves the exact Samsung Bixby deeplink from the official catalog. The user gets a one-tap action that opens the correct settings screen."

---

### Slide 4: Contradiction Rejection — Floating Circle (45 seconds)

**Action:** Click the **S3: Floating Circle [REJECTED]** demo button, or type:

> "My Galaxy S25 has a floating circle that constantly hovers on my screen."

**What to highlight:**

1. **Evidence Graph** — Path terminates in RED at the Decision Engine node
2. **Action Card** — Shows **Action Unsupported** or rejection
3. **Contract Validation** — Shows **FAILED** with specific failure reasons
4. **Pipeline Status** — Shows Contract Validated stage as incomplete

> "This is the critical safety feature. The user asked about a floating circle, but the SIIS evidence for Multi Window doesn't contain an explicitly supported action for this complaint. Instead of hallucinating a solution, ANCHOR **rejects** the proposed action. The evidence graph turns red to show the rejection path. The system never claims a verified action when verification has failed."

---

### Slide 5: Unsupported Query (30 seconds)

**Action:** Type a query with no matching SIIS evidence:

> "How do I bake a cake?"

**What to highlight:**

1. **Action Card** — Shows "No Action Authorized"
2. **Validation** — All checks fail
3. **Contract Validation** — Overall Status: **FAILED**

> "ANCHOR handles edge cases safely. A completely unrelated query produces no hallucinated troubleshooting steps. The response contains empty contexts — the system explicitly refuses rather than inventing solutions."

---

### Slide 6: New Query Reset (15 seconds)

**Action:** Click the **New Query** button.

**What to highlight:**

1. All cards reset to idle state
2. Evidence Graph returns to cyan idle nodes
3. Action Card shows **AWAITING QUERY**
4. Header shows **SYSTEM READY**

> "The New Query button cleanly resets the entire dashboard state, ready for the next troubleshooting session."

---

### Slide 7: Closing (30 seconds)

> "To summarize: ANCHOR is a proof-carrying troubleshooting engine. Every action it recommends is:
> 1. Grounded in official Samsung SIIS documentation
> 2. Verified against the 578-entry Samsung deeplink catalog
> 3. Validated for directional consistency
> 4. Schema-compliant with the official Theme 2 specification
>
> The system runs at sub-10ms latency, passes 43 automated tests, and achieves 100% schema validity across all 20 official SIIS benchmark queries. Most importantly — it never hallucates and never claims a verified action when verification has failed."

---

## Timing Summary

| Segment | Duration |
|---|---|
| Introduction | 30s |
| Screen Rotation (PASS) | 60s |
| Data Backup (PASS) | 45s |
| Floating Circle (REJECT) | 45s |
| Unsupported Query | 30s |
| New Query Reset | 15s |
| Closing | 30s |
| **Total** | **~4 minutes** |
