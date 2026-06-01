from fastapi import APIRouter
from pydantic import BaseModel

from app.services.explain_service import get_summary

router = APIRouter(tags=["summary"])


class SummaryPair(BaseModel):
    file1: str
    file2: str
    score: float
    level: str


class SummaryRequest(BaseModel):
    session_id: str
    pairs: list[SummaryPair]


class SummaryResponse(BaseModel):
    summary: str


@router.post("/summary", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest):
    """
    Generates a session-level AI summary for all similarity pairs.
    Returns a data-driven fallback if Ollama is not running.
    """
    pairs_as_dicts = [p.model_dump() for p in request.pairs]
    text = get_summary(pairs_as_dicts)
    return SummaryResponse(summary=text)
