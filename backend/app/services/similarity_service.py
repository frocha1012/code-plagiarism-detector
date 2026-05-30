"""
Handles cosine similarity computation between embeddings.
Day 3 task: implement compute_similarity().

Library: scikit-learn (cosine_similarity)
"""

from app.config import HIGH_SIMILARITY_THRESHOLD, MEDIUM_SIMILARITY_THRESHOLD


def compute_similarity(filenames: list[str], embeddings: list[list[float]]) -> list[dict]:
    """
    Compares every pair of embeddings.
    Returns a list of pairs sorted by similarity score descending.

    Each result dict: { file_a, file_b, score, level }
    level: "high" | "medium" | "low"
    """
    # TODO: use sklearn cosine_similarity on embedding matrix
    # TODO: iterate upper triangle of similarity matrix
    # TODO: assign level based on HIGH_SIMILARITY_THRESHOLD / MEDIUM_SIMILARITY_THRESHOLD
    # TODO: return sorted list of pairs
    raise NotImplementedError("Implement on Day 3")
