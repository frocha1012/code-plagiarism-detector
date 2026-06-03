# Analysis history routes.
# Lets the frontend list past analyses, reopen one, and delete it.

from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalysisResponse, HistoryItem
from app.services.history_service import (
    delete_session,
    get_analysis,
    list_history,
)

router = APIRouter(tags=["history"])


@router.get("/history", response_model=list[HistoryItem])
def get_history():
    """Returns metadata for every saved analysis, newest first."""
    return list_history()


@router.get("/history/{session_id}", response_model=AnalysisResponse)
def get_history_session(session_id: str):
    """Returns the stored analysis for a session so it can be reopened."""
    analysis = get_analysis(session_id)
    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail=f"No saved analysis found for session '{session_id}'.",
        )
    return analysis


@router.delete("/history/{session_id}")
def delete_history_session(session_id: str):
    """Deletes a session folder and all of its files."""
    if not delete_session(session_id):
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found.",
        )
    return {"deleted": session_id}
