"""
Optional AI explanation via local Ollama.

Calls the Ollama HTTP API to generate a short natural-language explanation
of why two files may be similar. If Ollama is not running or returns an
error, a static fallback is returned so the rest of the app is unaffected.
"""

import json
import urllib.error
import urllib.request

from app.config import OLLAMA_MODEL, OLLAMA_URL

_TIMEOUT_SECONDS = 20

_FALLBACK = (
    "Automated AI explanation is unavailable (Ollama is not running). "
    "Review the similarity score and the matched lines manually to assess "
    "whether the overlap is coincidental or indicates copied work."
)


def _build_prompt(file1: str, file2: str, score: float, level: str) -> str:
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
    """
    Returns a short AI explanation string.
    Falls back to a static message if Ollama is unavailable.
    """
    prompt = _build_prompt(file1, file2, score, level)
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
            if text:
                return text
            return _FALLBACK

    except (urllib.error.URLError, TimeoutError, OSError):
        return _FALLBACK

    except Exception:  # noqa: BLE001 — never crash the API over an optional feature
        return _FALLBACK
