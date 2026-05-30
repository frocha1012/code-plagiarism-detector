"""
Manual test: embedding generation + pairwise similarity.

Run from the backend/ directory:
    python tests/test_embeddings.py

Generates embeddings for all sample files, then computes cosine
similarity for every pair and prints the score and risk level.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.embedding_service import generate_embeddings
from app.services.similarity_service import compute_similarity

SAMPLE_DIR = Path(__file__).resolve().parent / "sample_files"


def main():
    files = sorted(SAMPLE_DIR.glob("*.py"))

    if not files:
        print(f"No .py files found in {SAMPLE_DIR}")
        return

    filenames = [f.name for f in files]
    print(f"Files: {filenames}\n")
    print("Generating embeddings (model loads from cache)...\n")

    snippets = [f.read_text(encoding="utf-8") for f in files]
    embeddings = generate_embeddings(snippets)

    print(f"Embedding dimensions: {len(embeddings[0])}\n")

    pairs = compute_similarity(filenames, embeddings, snippets)

    print("Pairwise similarity results:")
    print("-" * 50)
    for pair in pairs:
        print(f"{pair['file1']}  vs  {pair['file2']}")
        print(f"  semantic_score : {pair['semantic_score']}")
        print(f"  lexical_score  : {pair['lexical_score']}")
        print(f"  final_score    : {pair['score']}  [{pair['level']}]")
        print()
    print("-" * 50)


if __name__ == "__main__":
    main()
