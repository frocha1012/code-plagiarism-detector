# Upload routes.
# Handles file upload requests from the frontend.
# Routes only receive requests and delegate work to services/utils.

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models.schemas import UploadResponse
from app.services.upload_service import handle_upload

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_files(files: list[UploadFile] = File(...)):
    """
    Accepts multiple code files from the frontend.
    Validates extensions and file size.
    Saves files under uploads/<session_id>/.
    Returns session_id so the frontend can reference this batch later.
    """
    try:
        return await handle_upload(files)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
