"""
CodeBERT embedding generation.

Model: microsoft/codebert-base
Strategy: mean pooling over all real token embeddings.

Why mean pooling instead of [CLS] token:
  The [CLS] token embedding is designed for fine-tuned classification tasks.
  Without task-specific fine-tuning, [CLS] vectors cluster too close together,
  causing unrelated short files to score 0.99+ cosine similarity (false positives).

  Mean pooling averages every real token's hidden state, weighted by the
  attention mask so padding tokens are excluded. This produces vectors
  that reflect the actual content of the code, giving better separation
  between similar and unrelated files.

The tokenizer and model are loaded once on first use and
reused for all subsequent calls (module-level cache).
"""

import torch
from transformers import AutoTokenizer, AutoModel

MODEL_NAME = "microsoft/codebert-base"
MAX_TOKENS = 512  # CodeBERT's hard architectural limit

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


def _mean_pool(last_hidden_state: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    """
    Averages token embeddings, ignoring padding tokens.

    Expands the attention mask to match the hidden state shape,
    zeros out padding positions, sums real token embeddings,
    then divides by the number of real tokens.
    Result shape: (768,)
    """
    mask_expanded = attention_mask.unsqueeze(-1).float()
    sum_embeddings = (last_hidden_state * mask_expanded).sum(dim=1)
    real_token_count = mask_expanded.sum(dim=1).clamp(min=1e-9)
    return (sum_embeddings / real_token_count).squeeze()


def generate_embeddings(code_snippets: list[str]) -> list[list[float]]:
    """
    Takes a list of source code strings (one per file).
    Returns a list of 768-dimensional embedding vectors.

    Each vector is the mean of all real token embeddings from
    CodeBERT's last hidden state.
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

        vector = _mean_pool(outputs.last_hidden_state, inputs["attention_mask"])
        embeddings.append(vector.tolist())

    return embeddings
