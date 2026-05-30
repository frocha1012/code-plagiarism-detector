from fastapi import APIRouter, HTTPException

from app.config import LINE_MATCH_SIMILARITY_THRESHOLD
from app.models.schemas import CompareResponse, FileContentResponse
from app.utils.compare_utils import find_similar_lines
from app.utils.file_utils import get_session_file_path, read_file

router = APIRouter(tags=["files"])


@router.get("/files/{session_id}/{filename}", response_model=FileContentResponse)
def get_file_content(session_id: str, filename: str):
    """Returns the saved source code for a file inside an upload session."""
    try:
        file_path = get_session_file_path(session_id, filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return FileContentResponse(filename=file_path.name, content=read_file(file_path))


@router.get("/compare/{session_id}", response_model=CompareResponse)
def compare_files(session_id: str, file1: str, file2: str):
    """Returns similar line pairs for two files in the same upload session."""
    try:
        file1_path = get_session_file_path(session_id, file1)
        file2_path = get_session_file_path(session_id, file2)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    matches = find_similar_lines(
        read_file(file1_path),
        read_file(file2_path),
        LINE_MATCH_SIMILARITY_THRESHOLD,
    )

    return CompareResponse(file1=file1_path.name, file2=file2_path.name, matches=matches)
