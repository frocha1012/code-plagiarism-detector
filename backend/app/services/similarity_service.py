"""
Hybrid similarity computation: semantic + lexical.

Final score = (0.7 * semantic_score) + (0.3 * lexical_score)

semantic_score  — cosine similarity between CodeBERT mean-pool embeddings.
                  Captures structural and conceptual code similarity.

lexical_score   — Jaccard similarity over normalized token sets.
                  Captures surface-level token overlap after stripping
                  comments, lowercasing, and collapsing whitespace.

Why hybrid:
  CodeBERT embeddings alone cluster short files too close together, causing
  false positives. Adding a lexical component with 30% weight penalises
  pairs that share no real tokens, pulling unrelated files clearly below
  the suspicious threshold while keeping plagiarised pairs high.
"""

import re

from sklearn.metrics.pairwise import cosine_similarity

from app.config import HIGH_SIMILARITY_THRESHOLD, MEDIUM_SIMILARITY_THRESHOLD

SEMANTIC_WEIGHT = 0.7
LEXICAL_WEIGHT = 0.3


# ── Lexical helpers ──────────────────────────────────────────────────────────

def _normalize(code: str) -> str:
    """Remove comments, lowercase, and collapse whitespace."""
    code = re.sub(r"#.*", "", code)            # Python comments
    code = re.sub(r"//.*", "", code)           # JS / Java / C# line comments
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)  # block comments
    code = code.lower()
    code = re.sub(r"\s+", " ", code).strip()
    return code


def _tokenize(code: str) -> set[str]:
    """Extract identifier-like tokens from normalised code."""
    return set(re.findall(r"[a-z_][a-z0-9_]*", code))


def _jaccard(tokens_a: set[str], tokens_b: set[str]) -> float:
    """Jaccard similarity: |intersection| / |union|."""
    if not tokens_a and not tokens_b:
        return 1.0
    return len(tokens_a & tokens_b) / len(tokens_a | tokens_b)


# ── Level helper ─────────────────────────────────────────────────────────────

def _get_level(score: float) -> str:
    if score >= HIGH_SIMILARITY_THRESHOLD:
        return "high"
    if score >= MEDIUM_SIMILARITY_THRESHOLD:
        return "medium"
    return "low"


# ── Public API ────────────────────────────────────────────────────────────────

def compute_similarity(
    filenames: list[str],
    embeddings: list[list[float]],
    snippets: list[str],
) -> list[dict]:
    """
    Compares every pair of files using a hybrid semantic + lexical score.

    Returns a list of dicts sorted by final score descending.
    Each dict contains the public fields (file1, file2, score, level)
    plus debug fields (semantic_score, lexical_score) that are stripped
    from the API response by the Pydantic schema but available in tests.
    """
    if not (len(filenames) == len(embeddings) == len(snippets)):
        raise ValueError("filenames, embeddings, and snippets must all have the same length.")

    if len(embeddings) < 2:
        return []

    semantic_matrix = cosine_similarity(embeddings)
    token_sets = [_tokenize(_normalize(s)) for s in snippets]

    results = []

    for i in range(len(filenames)):
        for j in range(i + 1, len(filenames)):
            semantic = round(float(semantic_matrix[i][j]), 4)
            lexical = round(_jaccard(token_sets[i], token_sets[j]), 4)
            final = round(SEMANTIC_WEIGHT * semantic + LEXICAL_WEIGHT * lexical, 4)

            results.append(
                {
                    "file1": filenames[i],
                    "file2": filenames[j],
                    "score": final,
                    "level": _get_level(final),
                    # debug fields — stripped by Pydantic from API responses
                    "semantic_score": semantic,
                    "lexical_score": lexical,
                }
            )

    return sorted(results, key=lambda item: item["score"], reverse=True)
