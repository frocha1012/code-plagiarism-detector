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


class GithubCompareRequest(BaseModel):
    """Request body for comparing two public GitHub repositories."""
    repo_url_1: str
    repo_url_2: str


class SimilarityThresholds(BaseModel):
    """Similarity cut-offs (0–100%) sourced from the backend config."""
    high: float
    medium: float


class ProjectStatistics(BaseModel):
    """Aggregated, read-only usage stats for the About page."""
    total_analyses: int
    total_files: int
    total_high_risk_pairs: int
    total_reports: int | None = None  # not tracked yet — optional placeholder


class MetaResponse(BaseModel):
    """Configuration + statistics surfaced on the About / Methodology page."""
    thresholds: SimilarityThresholds
    statistics: ProjectStatistics
