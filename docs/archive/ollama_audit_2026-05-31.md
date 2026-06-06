# Ollama Integration Audit Report
**Date:** 2026-05-31
**Project:** Code Plagiarism Detector — University MVP

---

## 1. OLLAMA AVAILABILITY TEST — ✅ PASS

**Backend:** All network failure modes are caught. `explain_service.py` wraps the `urlopen` call in three catch layers: `URLError` (connection refused / DNS failure), `TimeoutError` / `OSError`, and a final bare `except Exception` safety net. Every path returns `_FALLBACK` string — the route always returns HTTP 200 with a valid `ExplainResponse`.

**Frontend:** `handleExplain` in `ResultsPage.jsx` has a `catch` block that writes a fallback string into `explanations[pairKey]`. The UI renders it through the same bullet-list component as a real response. No crash path exists.

**One weakness:** The fallback string is plain prose, not bullet-formatted. The frontend splits on `\n` and filters empty lines — a single-sentence fallback will render as one bullet item. The `li::before` CSS pseudo-element adds the dot anyway, so visually it is still acceptable.

---

## 2. OLLAMA SUCCESS TEST — ✅ PASS (with one note)

**Backend:** Request is correctly built — `model`, `prompt`, `stream: false`. Response is parsed as JSON, `.get("response", "")` handles missing keys, empty string falls back safely.

**Frontend loading state:** `loadingExplain` is set to `pairKey` before the fetch and cleared in `finally`. The spinner and "AI is thinking…" text render correctly while waiting. The button is `disabled` during the request so double-clicks are prevented.

**Response rendering:** The bullet splitter (`split("\n")`, strip `•`, filter empty) handles Ollama's output reasonably. Ollama sometimes outputs leading/trailing blank lines — `filter(Boolean)` handles that.

**One note:** The 20-second timeout is reasonable for `llama3.1` on most hardware. On a slow laptop during a live demo this could feel long.

---

## 3. RISK LEVEL BEHAVIOR — ✅ PASS

The `canCompare` flag is `pair.level === "high" || pair.level === "medium"`. Both the **✦ Explain with AI** button and the **Compare Files** button are gated behind this flag.

- **HIGH:** Explain button shown ✅, Compare button shown ✅
- **MEDIUM:** Explain button shown ✅, Compare button shown ✅
- **LOW:** Both buttons hidden ✅, replaced with "No significant similarities detected" ✅

---

## 4. MODEL SELECTION — ❌ NOT IMPLEMENTED

The model is hardcoded to `"llama3.1"` in `config.py`. There is no UI for selecting a model, and the backend always uses `OLLAMA_MODEL` from config regardless of what the frontend sends (the frontend doesn't send a model at all).

**Impact for demo:** Low — `llama3.1` is installed and working. Not a blocker.

**Minimal recommendation (not urgent):** A one-line dropdown on the Results page sending `model` in the request body, with the backend accepting an optional `model` field, would take ~20 minutes. Not needed for the demo.

---

## 5. ERROR HANDLING — ✅ PASS (with two minor weaknesses)

| Scenario | Backend | Frontend |
|---|---|---|
| Ollama unavailable | Returns fallback via `URLError` catch ✅ | Catch block writes fallback string ✅ |
| Invalid model | Ollama returns HTTP 404; `urlopen` raises `URLError` → fallback ✅ | Same ✅ |
| Timeout (>20s) | `TimeoutError` caught → fallback ✅ | Same ✅ |
| Empty response | `.get("response", "")` → empty string → `_FALLBACK` ✅ | Same ✅ |
| Malformed JSON | `json.loads` raises `ValueError` → caught by bare `except Exception` → fallback ✅ | Same ✅ |

**Weakness 1:** The bare `except Exception` suppresses all errors silently — including legitimate bugs during development. Not a runtime problem for the demo, but during development you could miss real issues.

**Weakness 2:** There is no user-facing distinction between "Ollama is offline" and "Ollama returned a bad response". Both show the same fallback text. Fine for the demo.

---

## 6. EXPLANATION QUALITY

**Old prompt output (first version — generic, no filenames):**
> "This high similarity score suggests structural similarity, as it is unlikely that two distinct programs would have such a high degree of code duplication without being direct copies or sharing a common algorithm."

**Current prompt** forces Ollama to reference actual filenames and the score in each bullet instruction. Expected output for `batch_01_library_original.py` vs `batch_02_library_renamed.py` at 92.7% should now look like:

> • The 92.7% score between 'batch_01_library_original.py' and 'batch_02_library_renamed.py' strongly suggests function and variable renaming with identical underlying logic preserved.
> • Check matching function signatures, loop structures, and dictionary key names across both files for systematic renaming.
> • Both students may have started from the same course-provided template or followed the same tutorial, leading to structurally identical solutions.
> • 92.7% exceeds the high-risk threshold; a reviewer must confirm whether renaming was deliberate obfuscation or an independent coincidence before any academic action.

**For MEDIUM (~0.82):** Prompt tier falls into "strong structural similarity with possible shared logic" — bullets should reflect partial match rather than full copy.

**Remaining quality risk:** Ollama does not always follow strict formatting instructions. It sometimes adds an intro line before the first bullet, or merges bullets. The frontend's `filter(Boolean)` handles blank lines, but an intro line would appear as an extra bullet.

---

## 7. FINAL READINESS ASSESSMENT

### What is working well
- Backend is fully isolated — `/api/explain` never crashes the app
- Fallback path is clean and renders correctly in the UI
- Loading state, spinner, disabled button, and result caching all work correctly
- Risk-level gating (only high/medium get the button) is correctly implemented
- Prompt includes filenames and score tier to push toward specific output

### Remaining issues
1. **Bullet format not guaranteed** — Ollama may prepend an intro sentence which renders as an extra bullet. Fixable with a simple response post-processor that strips any line not starting with `•`.
2. **Fallback text is not bullet-formatted** — Shows as one plain `<li>` instead of the styled list. Minor visual inconsistency.
3. **No model selection UI** — Config-only, fine for the demo.

### Critical blockers
None. The feature works end-to-end.

### Nice-to-have improvements
- Post-process the Ollama response to strip non-bullet lines before returning
- Format the fallback as a single bullet so it renders consistently
- Add a timeout indicator ("This may take up to 20 seconds") near the spinner

### Demo readiness: ✅ READY
The integration is stable and safe. The only live risk is Ollama producing a stray intro line — easily fixed in one line of code when needed. For the demo it is unlikely to be noticed.
