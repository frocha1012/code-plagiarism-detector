"""
Manual test script for embedding generation.

Run from the backend/ directory:
    python tests/test_embeddings.py

First run will download microsoft/codebert-base (~500 MB).
Subsequent runs use the cached model from ~/.cache/huggingface/.
"""

import sys
from pathlib import Path

# Allow imports from app/ when running this script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.embedding_service import generate_embeddings

SAMPLE_DIR = Path(__file__).resolve().parent / "sample_files"


def main():
    files = sorted(SAMPLE_DIR.glob("*.py"))

    if not files:
        print(f"No .py files found in {SAMPLE_DIR}")
        return

    print(f"Found {len(files)} file(s): {[f.name for f in files]}\n")
    print("Loading model and generating embeddings...")
    print("(First run downloads ~500 MB — this may take a minute)\n")

    snippets = [f.read_text(encoding="utf-8") for f in files]
    embeddings = generate_embeddings(snippets)

    print("Results:")
    print("-" * 40)
    for file, embedding in zip(files, embeddings):
        print(f"{file.name}: {len(embedding)} dimensions")

    print("-" * 40)
    print("Done. Embedding generation works correctly.")


if __name__ == "__main__":
    main()
