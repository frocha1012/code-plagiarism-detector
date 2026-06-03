# Similarity routes.
# Accepts a session_id, loads the uploaded files, generates embeddings,
# computes cosine similarity, and returns ranked pairs.

from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalysisResponse
from app.services.embedding_service import generate_embeddings
from app.services.history_service import save_analysis
from app.services.similarity_service import compute_similarity
from app.utils.file_utils import list_session_files, read_file

router = APIRouter(tags=["similarity"])


@router.post("/analyze", response_model=AnalysisResponse)
def analyze(session_id: str):
    """
    Loads files for the given session_id, generates CodeBERT embeddings,
    computes pairwise cosine similarity, and returns all pairs with
    their similarity score and risk level.
    """
    files = list_session_files(session_id)

    if not files:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found or contains no files.",
        )

    if len(files) < 2:
        raise HTTPException(
            status_code=400,
            detail="Session must contain at least 2 files to compare.",
        )

    filenames = [f.name for f in files]
    snippets = [read_file(f) for f in files]

    embeddings = generate_embeddings(snippets)
    pairs = compute_similarity(filenames, embeddings, snippets)

    # Persist metadata + results so this analysis appears in History.
    save_analysis(session_id, pairs)

    return AnalysisResponse(session_id=session_id, pairs=pairs)
