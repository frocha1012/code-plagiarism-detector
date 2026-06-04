# GitHub repository comparison route.
# Downloads two public repositories and feeds them into the existing
# similarity pipeline. Returns the same shape as POST /api/analyze.

from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalysisResponse, GithubCompareRequest
from app.services.github_service import compare_repositories

router = APIRouter(tags=["github"])


@router.post("/github/compare", response_model=AnalysisResponse)
def github_compare(request: GithubCompareRequest):
    """
    Compares source code between two public GitHub repositories.

    Downloads each repository as a ZIP archive, extracts supported source
    files into a normal session, and runs the existing embedding + similarity
    pipeline. Results are saved to History and returned for the Results page.
    """
    try:
        return compare_repositories(request.repo_url_1, request.repo_url_2)
    except ValueError as exc:
        # User-friendly validation / download / limit errors.
        raise HTTPException(status_code=400, detail=str(exc)) from exc
