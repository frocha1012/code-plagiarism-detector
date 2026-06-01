"""
Optional AI features via local Ollama.

Provides per-pair explanations and a session-level summary.
All functions fall back gracefully if Ollama is unavailable.
"""

import json
import urllib.error
import urllib.request

from app.config import OLLAMA_MODEL, OLLAMA_URL

_TIMEOUT_SECONDS = 20

_FALLBACK_EXPLAIN = (
    "Automated AI explanation is unavailable (Ollama is not running). "
    "Review the similarity score and the matched lines manually to assess "
    "whether the overlap is coincidental or indicates copied work."
)


# ── Shared Ollama caller ──────────────────────────────────────────────────────

def _call_ollama(prompt: str, fallback: str) -> str:
    """Sends a prompt to the local Ollama API and returns the response text.
    Returns fallback if Ollama is unavailable or returns an empty response."""
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }).encode()

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT_SECONDS) as response:
            body = json.loads(response.read().decode())
            text = body.get("response", "").strip()
            return text if text else fallback

    except (urllib.error.URLError, TimeoutError, OSError):
        return fallback

    except Exception:  # noqa: BLE001 — never crash the API over an optional feature
        return fallback


# ── Per-pair explanation ──────────────────────────────────────────────────────

def _build_explain_prompt(file1: str, file2: str, score: float, level: str) -> str:
    pct = f"{score * 100:.1f}%"

    if score >= 0.95:
        similarity_type = "near-identical copy or trivial variable renaming"
    elif score >= 0.88:
        similarity_type = "likely variable or function renaming with preserved logic"
    else:
        similarity_type = "strong structural similarity with possible shared logic"

    return (
        f"You are a university lecturer reviewing a plagiarism detection report.\n\n"
        f"The detector compared two student files:\n"
        f"  '{file1}' vs '{file2}'\n"
        f"  Hybrid similarity score: {pct} — classified as {level} risk.\n"
        f"  At this score range, the pattern is most consistent with: {similarity_type}.\n\n"
        f"Write exactly 4 bullet points. Each bullet MUST reference the actual filenames or score.\n"
        f"Start each line with '• '. No intro. No outro. No generic filler.\n\n"
        f"• Bullet 1: What the {pct} score between '{file1}' and '{file2}' specifically suggests about how the code was copied or modified.\n"
        f"• Bullet 2: Name 2-3 concrete things to check inside these files (e.g. function names, loop structure, variable names).\n"
        f"• Bullet 3: The most plausible innocent explanation for this specific score (shared starter code, same tutorial, etc.).\n"
        f"• Bullet 4: One sentence on why {pct} is flagged as {level} risk and what a human reviewer must confirm before drawing conclusions.\n\n"
        f"Be direct, specific, and professional. One sentence per bullet."
    )


def get_explanation(file1: str, file2: str, score: float, level: str) -> str:
    """Returns a 4-bullet AI explanation for a similarity pair."""
    prompt = _build_explain_prompt(file1, file2, score, level)
    return _call_ollama(prompt, _FALLBACK_EXPLAIN)


# ── Session-level summary ─────────────────────────────────────────────────────

def _build_summary_prompt(pairs: list[dict]) -> str:
    total_files = len({f for p in pairs for f in (p["file1"], p["file2"])})
    total_pairs = len(pairs)
    high_pairs = [p for p in pairs if p["level"] == "high"]
    medium_pairs = [p for p in pairs if p["level"] == "medium"]
    highest = max(pairs, key=lambda p: p["score"]) if pairs else None
    high_count = len(high_pairs)
    medium_count = len(medium_pairs)

    top_pair_line = ""
    if highest:
        pct = f"{highest['score'] * 100:.1f}%"
        top_pair_line = (
            f"  Most suspicious pair: '{highest['file1']}' vs '{highest['file2']}' "
            f"at {pct} ({highest['level']} risk).\n"
        )

    high_list = "\n".join(
        f"  - '{p['file1']}' vs '{p['file2']}': {p['score'] * 100:.1f}%"
        for p in high_pairs
    )

    return (
        f"You are a university lecturer reviewing a plagiarism detection report.\n\n"
        f"Session statistics:\n"
        f"  Files analyzed: {total_files}\n"
        f"  Total pairs compared: {total_pairs}\n"
        f"  High-risk pairs: {high_count}\n"
        f"  Medium-risk pairs: {medium_count}\n"
        f"{top_pair_line}"
        + (f"\nHigh-risk pairs:\n{high_list}\n" if high_list else "")
        + f"\nWrite a concise report in 2–3 short paragraphs covering:\n"
        f"  1. An overall assessment of the session (how many files, how many suspicious pairs).\n"
        f"  2. The most concerning findings and what patterns they suggest.\n"
        f"  3. A recommendation on which pairs warrant manual review and why.\n\n"
        f"End with this exact sentence on its own line:\n"
        f"'Similarity scores are indicators and do not constitute proof of plagiarism.'\n\n"
        f"Be professional, specific, and concise. Reference actual filenames and scores."
    )


def _build_fallback_summary(pairs: list[dict]) -> str:
    total_files = len({f for p in pairs for f in (p["file1"], p["file2"])})
    total_pairs = len(pairs)
    high_count = sum(1 for p in pairs if p["level"] == "high")
    medium_count = sum(1 for p in pairs if p["level"] == "medium")
    highest = max(pairs, key=lambda p: p["score"]) if pairs else None

    lines = [
        f"This session analyzed {total_files} files across {total_pairs} pairwise comparisons. "
        f"{high_count} pair(s) were flagged as high risk and {medium_count} as medium risk.",
    ]

    if highest:
        pct = f"{highest['score'] * 100:.1f}%"
        lines.append(
            f"The most suspicious pair was '{highest['file1']}' vs '{highest['file2']}' "
            f"with a similarity score of {pct}. "
            f"This pair should be prioritized for manual review."
        )

    if high_count > 0:
        lines.append(
            "All high-risk pairs are recommended for manual review by a lecturer "
            "before any academic decision is made."
        )

    lines.append(
        "Similarity scores are indicators and do not constitute proof of plagiarism."
    )

    return " ".join(lines)


def get_summary(pairs: list[dict]) -> str:
    """Returns an AI-generated session summary, or a data-driven fallback."""
    if not pairs:
        return "No similarity pairs were provided. Upload and analyze files to generate a summary."

    fallback = _build_fallback_summary(pairs)
    prompt = _build_summary_prompt(pairs)
    return _call_ollama(prompt, fallback)
