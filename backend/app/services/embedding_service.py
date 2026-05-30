"""
CodeBERT embedding generation.

Model: microsoft/codebert-base
Strategy: extract the [CLS] token from the last hidden state.
          This vector represents the entire code snippet.

The tokenizer and model are loaded once on first use and
reused for all subsequent calls (module-level cache).
"""

import torch
from transformers import AutoTokenizer, AutoModel

MODEL_NAME = "microsoft/codebert-base"
MAX_TOKENS = 512  # CodeBERT's hard limit

_tokenizer = None
_model = None


def _load_model():
    """Loads and caches the tokenizer and model on first call."""
    global _tokenizer, _model

    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModel.from_pretrained(MODEL_NAME)
        _model.eval()

    return _tokenizer, _model


def generate_embeddings(code_snippets: list[str]) -> list[list[float]]:
    """
    Takes a list of source code strings (one per file).
    Returns a list of 768-dimensional embedding vectors.

    Each vector is the [CLS] token from CodeBERT's last hidden state,
    which encodes the meaning of the entire code snippet.
    """
    tokenizer, model = _load_model()
    embeddings = []

    for snippet in code_snippets:
        inputs = tokenizer(
            snippet,
            return_tensors="pt",
            truncation=True,
            max_length=MAX_TOKENS,
            padding=True,
        )

        with torch.no_grad():
            outputs = model(**inputs)

        # Shape: (1, seq_len, 768) → take index 0 → (768,)
        cls_vector = outputs.last_hidden_state[:, 0, :].squeeze()
        embeddings.append(cls_vector.tolist())

    return embeddings
