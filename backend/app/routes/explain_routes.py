from fastapi import APIRouter
from pydantic import BaseModel

from app.services.explain_service import get_explanation

router = APIRouter(tags=["explain"])


class ExplainRequest(BaseModel):
    session_id: str
    file1: str
    file2: str
    score: float
    level: str


class ExplainResponse(BaseModel):
    explanation: str


@router.post("/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest):
    """
    Generates a short AI explanation for a similarity pair using local Ollama.
    Returns a graceful fallback message if Ollama is not running.
    """
    text = get_explanation(
        request.file1,
        request.file2,
        request.score,
        request.level,
    )
    return ExplainResponse(explanation=text)
