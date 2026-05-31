# Upload business logic.
# Keeps the route thin while file operations stay inside file_utils.py.

from pathlib import Path

from fastapi import UploadFile

from app.utils.file_utils import extract_zip, new_session_id, save_upload


async def handle_upload(files: list[UploadFile]) -> dict:
    """
    Creates an upload session and saves every uploaded file.

    Accepts either:
    - A single .zip archive (extracted into the session folder), or
    - Two or more individual source code files.

    Returns the response payload used by the upload route.
    """
    is_zip_upload = (
        len(files) == 1
        and Path(files[0].filename or "").suffix.lower() == ".zip"
    )

    session_id = new_session_id()

    if is_zip_upload:
        zip_bytes = await files[0].read()
        uploaded_files = extract_zip(zip_bytes, session_id)
    else:
        if len(files) < 2:
            raise ValueError(
                "Upload at least 2 source files, or a single ZIP archive."
            )
        uploaded_files = []
        for file in files:
            saved_path = await save_upload(file, session_id)
            uploaded_files.append(saved_path.name)

    return {
        "session_id": session_id,
        "uploaded_files": uploaded_files,
        "file_count": len(uploaded_files),
    }
