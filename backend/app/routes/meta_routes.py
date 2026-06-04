# Project metadata routes.
# Exposes similarity thresholds (from config) and aggregated usage stats
# so the About / Methodology page can stay in sync with the real backend
# instead of hardcoding values. Read-only; touches no analysis flow.

from fastapi import APIRouter

from app.config import HIGH_SIMILARITY_THRESHOLD, MEDIUM_SIMILARITY_THRESHOLD
from app.models.schemas import (
    MetaResponse,
    ProjectStatistics,
    SimilarityThresholds,
)
from app.services.history_service import get_statistics

router = APIRouter(tags=["meta"])


@router.get("/meta", response_model=MetaResponse)
def get_meta():
    """Returns similarity thresholds and project statistics for the About page."""
    return MetaResponse(
        thresholds=SimilarityThresholds(
            high=round(HIGH_SIMILARITY_THRESHOLD * 100, 1),
            medium=round(MEDIUM_SIMILARITY_THRESHOLD * 100, 1),
        ),
        statistics=ProjectStatistics(**get_statistics()),
    )
