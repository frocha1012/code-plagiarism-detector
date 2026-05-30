# Pydantic schemas for request/response validation.
# FastAPI uses these to auto-validate data and generate /docs.

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Returned after a successful file upload."""
    session_id: str
    uploaded_files: list[str]
    file_count: int


class SimilarityPair(BaseModel):
    """A single comparison result between two files."""
    file_a: str
    file_b: str
    score: float          # cosine similarity value between 0 and 1
    level: str            # "high" | "medium" | "low"


class AnalysisResponse(BaseModel):
    """Returned after similarity analysis completes."""
    session_id: str
    pairs: list[SimilarityPair]
