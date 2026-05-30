# File utility helpers.
# Handles session directories, file saving, and file reading.
# Keeps file I/O logic out of routes and services.

import uuid
from pathlib import Path
from fastapi import UploadFile

from app.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE


def new_session_id() -> str:
    """Generates a unique ID for each upload batch."""
    return str(uuid.uuid4())


def get_session_dir(session_id: str) -> Path:
    """Returns (and creates) the folder for a given session."""
    session_dir = UPLOAD_FOLDER / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def is_allowed_file(filename: str) -> bool:
    """Returns True if the file extension is in the allowed set."""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def _safe_filename(filename: str) -> str:
    """Removes any folder path from the uploaded filename."""
    return Path(filename).name


def _unique_destination(session_dir: Path, filename: str) -> Path:
    """Avoids overwriting files with the same name in one upload session."""
    destination = session_dir / filename
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        candidate = session_dir / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


async def save_upload(file: UploadFile, session_id: str) -> Path:
    """
    Saves an uploaded file to uploads/<session_id>/<filename>.
    Raises ValueError if the extension or size is not allowed.
    Returns the saved file path.
    """
    filename = _safe_filename(file.filename or "")

    if not filename:
        raise ValueError("Uploaded file is missing a filename.")

    if not is_allowed_file(filename):
        raise ValueError(f"File type not allowed: {filename}")

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {filename}")

    session_dir = get_session_dir(session_id)
    destination = _unique_destination(session_dir, filename)
    destination.write_bytes(content)
    return destination


def read_file(path: Path) -> str:
    """Reads a saved file as a UTF-8 string."""
    return path.read_text(encoding="utf-8", errors="ignore")


def list_session_files(session_id: str) -> list[Path]:
    """Returns all file paths saved under a session directory."""
    session_dir = UPLOAD_FOLDER / session_id
    if not session_dir.exists():
        return []
    return list(session_dir.iterdir())


def get_session_file_path(session_id: str, filename: str) -> Path:
    """
    Safely resolves a file path inside a session folder.
    Raises ValueError for traversal attempts or missing files.
    """
    safe_name = _safe_filename(filename)
    if not safe_name or safe_name != filename:
        raise ValueError("Invalid filename.")

    session_dir = (UPLOAD_FOLDER / session_id).resolve()
    file_path = (session_dir / safe_name).resolve()

    if session_dir not in file_path.parents:
        raise ValueError("Invalid file path.")

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {safe_name}")

    return file_path
