"""
Handles CodeBERT embedding generation.
Day 2 task: implement generate_embeddings().

Model: microsoft/codebert-base
Library: transformers (HuggingFace)
"""


def generate_embeddings(code_snippets: list[str]) -> list[list[float]]:
    """
    Takes a list of code strings.
    Returns a list of embedding vectors (one per file).
    """
    # TODO: load tokenizer and model (cache after first load)
    # TODO: tokenize each snippet
    # TODO: run forward pass, extract [CLS] token as embedding
    # TODO: return list of float vectors
    raise NotImplementedError("Implement on Day 2")
