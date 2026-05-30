from fastapi import APIRouter

router = APIRouter(tags=["similarity"])


@router.post("/analyze")
async def analyze(session_id: str):
    """
    Triggers embedding generation + cosine similarity for a set of uploaded files.
    Day 2-3 task: wire embedding_service and similarity_service here.
    """
    # TODO: load files for session_id
    # TODO: call embedding_service.generate_embeddings()
    # TODO: call similarity_service.compute_similarity()
    # TODO: return ranked suspicious pairs
    return {"session_id": session_id, "results": []}


@router.get("/results/{session_id}")
async def get_results(session_id: str):
    """
    Returns cached similarity results for a session.
    Day 4 task: serve results to the frontend results page.
    """
    # TODO: retrieve results from in-memory store or temp file
    return {"session_id": session_id, "pairs": []}
