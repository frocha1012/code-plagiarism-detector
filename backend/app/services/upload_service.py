# Upload business logic.
# Keeps the route thin while file operations stay inside file_utils.py.

from fastapi import UploadFile

from app.utils.file_utils import new_session_id, save_upload


async def handle_upload(files: list[UploadFile]) -> dict:
    """
    Creates an upload session and saves every uploaded file.
    Returns the response payload used by the upload route.
    """
    if len(files) < 2:
        raise ValueError("Upload at least 2 files to compare.")

    session_id = new_session_id()
    uploaded_files = []

    for file in files:
        saved_path = await save_upload(file, session_id)
        uploaded_files.append(saved_path.name)

    return {
        "session_id": session_id,
        "uploaded_files": uploaded_files,
        "file_count": len(uploaded_files),
    }
