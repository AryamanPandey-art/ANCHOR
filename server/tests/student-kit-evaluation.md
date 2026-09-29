# ANCHOR — Official 20-Query Evaluation Matrix (Theme 2 Student Kit)

**Generated:** 2026-09-27T14:31:24.429Z  
**Dataset:** `server/data/student-kit/input.txt` (20 Official Samsung PRISM Queries)  
**Total Queries:** 20  
**VERIFIED (PASS):** 19  
**REJECTED (FAIL):** 1  
**Hallucination Check:** CLEAN (0 invented records, 0 fake deeplinks)

---

## Evaluation Summary Table

| # | Query Snippet | Identified Intent | Target Dir | Grounded SIIS | Resolved Action | Official Deeplink | Final Verdict |
|---|---|---|---|---|---|---|---|
| 1 | "My TechCorp A15G tablet screen flashes and..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_1` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 2 | "My Nexa X1 screen turns completely blank o..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_10` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 3 | "My Nexa Fold X1 screen went completely bla..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_5` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 4 | "My TechCorp Nexa A14/A15 screen suddenly w..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_2` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 5 | "My tablet screen stays completely blank wh..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_1` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 6 | "My tablet's screen stays dark and only thr..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_10` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 7 | "My new smartphone's main screen stays smal..." | `DISPLAY_ASPECT_RATIO` | `ENABLE` | `#SIIS-ROW_9` | Enable Touch Sensitivity | `act/14eb42b895` | **VERIFIED (PASS)** |
| 8 | "My Nexa Fold X1 inner screen stopped worki..." | `TOUCH_SENSITIVITY` | `DISABLE` | `#SIIS-ROW_9` | Disable Touch Sensitivity | `act/1b0d34e9b4` | **VERIFIED (PASS)** |
| 9 | "My TechCorp Nexa Fold X1 screen flickers a..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_2` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 10 | "My Nexa Fold X1 screen is half black—one s..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_2` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 11 | "My Nexa X1 has a floating circle that cons..." | `MULTI_WINDOW` | `DISABLE` | `#SIIS-ROW_7` | Customize the Quick Access panel | `None` | **REJECTED (FAIL)** |
| 12 | "My Nexa X1 screen stays blank and doesn't ..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_2` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 13 | "My smartphone's screen is completely crack..." | `CRACKED_SCREEN` | `ENABLE` | `#SIIS-ROW_14` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 14 | "My Nexa X1 Ultra only shows a blue (or bla..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_10` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 15 | "My TechCorp X1 Ultra screen flashes extrem..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_10` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 16 | "1. "My Nexa X1 screen goes completely blan..." | `BLANK_DISPLAY` | `ENABLE` | `#SIIS-ROW_5` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |
| 17 | "1. "My Nexa Fold X1 screen is cracked agai..." | `TOUCH_SENSITIVITY` | `ENABLE` | `#SIIS-ROW_9` | Enable Touch Sensitivity | `act/14eb42b895` | **VERIFIED (PASS)** |
| 18 | "My Nexa A14 screen looks distorted right a..." | `SCREEN_ROTATION` | `ENABLE` | `#SIIS-ROW_20` | Enable Auto Rotate | `act/7c340914be` | **VERIFIED (PASS)** |
| 19 | "My Nexa X1 screen inputs are delayed and t..." | `TOUCH_SENSITIVITY` | `ENABLE` | `#SIIS-ROW_9` | Enable Touch Sensitivity | `act/14eb42b895` | **VERIFIED (PASS)** |
| 20 | "My Nexa X1 Ultra screen is completely blac..." | `CRACKED_SCREEN` | `ENABLE` | `#SIIS-ROW_14` | Back Up Phone Data | `act/b3ed3ed663` | **VERIFIED (PASS)** |

---

## Detailed Query Reports

### Query 01

**Input Query:**  
> "My TechCorp A15G tablet screen flashes and then goes completely blank whenever I tap to open an email in Gmail, and after it works for a short time it goes blank again."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Tablet (Galaxy Tab)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_1`  
  - Title: Email server not responding on smartphone or tablet  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 02

**Input Query:**  
> "My Nexa X1 screen turns completely blank or white and no text appears when I search for a stock price or use the Quick Assist app, and it happens with other apps too."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_10`  
  - Title: Screen flickers when using the Camera on a smartphone  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 03

**Input Query:**  
> "My Nexa Fold X1 screen went completely black, so I can't see or interact with the phone, and I'm unable to use Data Transfer or any other method to transfer my data."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Foldable (Galaxy Fold)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_5`  
  - Title: Transfer Secure folder with Data Transfer  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 04

**Input Query:**  
> "My TechCorp Nexa A14/A15 screen suddenly went completely black on its own after about a month of use. It doesn't display anything, even when I try to turn it on."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_2`  
  - Title: Blank or black display on a smartphone or tablet  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 05

**Input Query:**  
> "My tablet screen stays completely blank when I try to use Data Transfer to scan the QR code for transferring data from my Nexa X1 phone, so the transfer can't proceed."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Tablet (Galaxy Tab)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_1`  
  - Title: Email server not responding on smartphone or tablet  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 06

**Input Query:**  
> "My tablet's screen stays dark and only three app icons are lit while the rest are dark and won't open, so nothing loads on the screen and I can't use the device."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Tablet (Galaxy Tab)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_10`  
  - Title: Screen flickers when using the Camera on a smartphone  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 07

**Input Query:**  
> "My new smartphone's main screen stays small and doesn't fill the whole display; I can't make it expand to full size and I've never seen this before."

- **Intent:** `DISPLAY_ASPECT_RATIO` (Display & Screen Mirroring)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_9`  
  - Title: Access your smartphone's data if the screen does not respond  
  - Relevance: 70%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Enable Touch Sensitivity  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS row_21 specifies navigating to Settings > Display and enabling Touch sensitivity for screen protectors.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/14eb42b895`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 08

**Input Query:**  
> "My Nexa Fold X1 inner screen stopped working by itself; it shows no image and doesn't respond to touch, while the outer cover screen still works."

- **Intent:** `TOUCH_SENSITIVITY` (Display & Touch)  
- **Target Direction:** `DISABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_9`  
  - Title: Access your smartphone's data if the screen does not respond  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Disable Touch Sensitivity  
  - Action Direction: `DISABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS row_21 specifies navigating to Settings > Display and disabling Touch sensitivity when no film is used.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/1b0d34e9b4`  
  - Catalog Match: `VALID`  
  - Direction: `DISABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 09

**Input Query:**  
> "My TechCorp Nexa Fold X1 screen flickers and goes blank whenever I open it, so I can't see anything or access the settings, which stops me from using the phone."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Foldable (Galaxy Fold)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_2`  
  - Title: Blank or black display on a smartphone or tablet  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 10

**Input Query:**  
> "My Nexa Fold X1 screen is half black—one side of the display is completely dark while the other side works fine, so I can't access the device normally."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Foldable (Galaxy Fold)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_2`  
  - Title: Blank or black display on a smartphone or tablet  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 11

**Input Query:**  
> "My Nexa X1 has a floating circle that constantly hovers on my screen and gives me quick shortcuts to recent apps, home, back, screen off, volume control, and more; I want to remove it."

- **Intent:** `MULTI_WINDOW` (Accessibility & Navigation)  
- **Target Direction:** `DISABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_7`  
  - Title: Use Multi window and App pairs on your smartphone or tablet  
  - Relevance: 85%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Customize the Quick Access panel  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS row_7 prescribes: Customize the Quick Access panel  
- **Deeplink Resolution:**  
  - URI: `None`  
  - Catalog Match: `INVALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: NO ✕  
- **Contract Guard:**  
  - Overall Status: **FAIL**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: FAIL ✕  
  - Direction Check: FAIL ✕  
  - Schema Check: FAIL ✕  
  - Failure Reasons:  
    - ❌ *No matching Samsung catalog deeplink found for action 'Customize the Quick Access panel' with direction 'ENABLE'.*  
    - ❌ *Direction does not match the user's request.*  
    - ❌ *Schema validation failed: Prerequisites not met to build official ContextDeeplinkResponse.*  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **REJECTED (FAIL)**  

---

### Query 12

**Input Query:**  
> "My Nexa X1 screen stays blank and doesn't show any activation message or anything else when I turn it on after the carrier deactivated the old phone."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_2`  
  - Title: Blank or black display on a smartphone or tablet  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 13

**Input Query:**  
> "My smartphone's screen is completely cracked, it's a total crack and I can't use the device."

- **Intent:** `CRACKED_SCREEN` (Hardware & Service)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_14`  
  - Title: Cracked or bleeding screen on smartphone or tablet  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 14

**Input Query:**  
> "My Nexa X1 Ultra only shows a blue (or black) screen with tiny text when I try to turn it on, and it won't start up. I tried holding the power button but it doesn't help."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_10`  
  - Title: Screen flickers when using the Camera on a smartphone  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 15

**Input Query:**  
> "My TechCorp X1 Ultra screen flashes extremely quickly (in milliseconds) whenever I plug in a charger, making the display unusable for a short period."

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_10`  
  - Title: Screen flickers when using the Camera on a smartphone  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 16

**Input Query:**  
> "1. "My Nexa X1 screen goes completely blank, just a dark screen with occasional scrolling and no visible content, so I can't see anything or use Data Transfer to transfer data.""

- **Intent:** `BLANK_DISPLAY` (Display & Power)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_5`  
  - Title: Transfer Secure folder with Data Transfer  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 17

**Input Query:**  
> "1. "My Nexa Fold X1 screen is cracked again right where it folds." 2. "The touch doesn't work on certain parts of the screen." 3. "I can hardly see anything on the display.""

- **Intent:** `TOUCH_SENSITIVITY` (Display & Touch)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_9`  
  - Title: Access your smartphone's data if the screen does not respond  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Enable Touch Sensitivity  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS row_21 specifies navigating to Settings > Display and enabling Touch sensitivity for screen protectors.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/14eb42b895`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 18

**Input Query:**  
> "My Nexa A14 screen looks distorted right after I received the phone, and I need a diagnostic test."

- **Intent:** `SCREEN_ROTATION` (Display & Rotation)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_20`  
  - Title: Screen does not rotate on smartphone or tablet  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Enable Auto Rotate  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS row_20 prescribes adjusting screen orientation settings in Quick settings to Auto rotate to allow automatic rotation.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/7c340914be`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 19

**Input Query:**  
> "My Nexa X1 screen inputs are delayed and the touch responsiveness is laggy, causing a noticeable delay when I try to interact with the phone."

- **Intent:** `TOUCH_SENSITIVITY` (Display & Touch)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_9`  
  - Title: Access your smartphone's data if the screen does not respond  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Enable Touch Sensitivity  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS row_21 specifies navigating to Settings > Display and enabling Touch sensitivity for screen protectors.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/14eb42b895`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

### Query 20

**Input Query:**  
> "My Nexa X1 Ultra screen is completely black and won't turn on, even though the phone powers on, rings, and otherwise works; there is no physical damage."

- **Intent:** `CRACKED_SCREEN` (Hardware & Service)  
- **Target Direction:** `ENABLE`  
- **Device Type:** Smartphone (Galaxy)  
- **Evidence:**  
  - SIIS ID: `#SIIS-ROW_14`  
  - Title: Cracked or bleeding screen on smartphone or tablet  
  - Relevance: 98%  
  - Grounded: YES ✔  
  - Provenance: Samsung Student Kit (siis_responses.json)  
- **Action Proposal:**  
  - AI Proposed Action: Back Up Phone Data  
  - Action Direction: `ENABLE`  
  - Resolved: YES ✔  
  - Proof: SIIS prescribes backing up data prior to hardware inspection or service reset.  
- **Deeplink Resolution:**  
  - URI: `voiceassist://masked/act/b3ed3ed663`  
  - Catalog Match: `VALID`  
  - Direction: `ENABLE`  
  - Verified in Catalog: YES ✔  
- **Contract Guard:**  
  - Overall Status: **PASS**  
  - Grounding Check: PASS ✔  
  - Deeplink Check: PASS ✔  
  - Direction Check: PASS ✔  
  - Schema Check: PASS ✔  
- **Official Schema (schema.py):** VALID ✔ (Validated via Python Pydantic ContextDeeplinkResponse)  
- **Final Decision:** **VERIFIED (PASS)**  

---

