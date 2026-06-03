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
    file1: str
    file2: str
    score: float   # cosine similarity, 0.0 – 1.0
    level: str     # "high" | "medium" | "low"


class AnalysisResponse(BaseModel):
    """Returned after similarity analysis completes."""
    session_id: str
    pairs: list[SimilarityPair]


class FileContentResponse(BaseModel):
    """Returned when loading a file for side-by-side comparison."""
    filename: str
    content: str


class LineMatch(BaseModel):
    """A similar line pair for the compare view."""
    file1_line: int
    file1_text: str
    file2_line: int
    file2_text: str
    similarity: float


class CompareResponse(BaseModel):
    """Returned when comparing two files line-by-line."""
    file1: str
    file2: str
    matches: list[LineMatch]


class HistoryItem(BaseModel):
    """Metadata for a single saved analysis, used by the History page."""
    session_id: str
    created_at: str
    file_count: int
    highest_score: float
    high_risk_pairs: int
