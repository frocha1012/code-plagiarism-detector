# Analysis history business logic.
# Persists a small metadata.json + analysis.json inside each session folder
# so past analyses can be listed, reopened, and deleted.
# No database — the existing uploads folder is the only storage.

import json
import shutil
from datetime import datetime, timezone

from app.config import UPLOAD_FOLDER
from app.utils.file_utils import (
    METADATA_FILE,
    ANALYSIS_FILE,
    list_session_files,
)


def _public_pairs(pairs: list[dict]) -> list[dict]:
    """Keeps only the fields the frontend needs (drops debug fields)."""
    return [
        {
            "file1": p["file1"],
            "file2": p["file2"],
            "score": p["score"],
            "level": p["level"],
        }
        for p in pairs
    ]


def save_analysis(session_id: str, pairs: list[dict]) -> None:
    """
    Writes metadata.json and analysis.json into the session folder.
    Called right after a similarity analysis completes.
    """
    session_dir = UPLOAD_FOLDER / session_id
    if not session_dir.exists():
        return

    clean_pairs = _public_pairs(pairs)
    file_count = len(list_session_files(session_id))
    highest_score = max((p["score"] for p in clean_pairs), default=0.0)
    high_risk_pairs = sum(1 for p in clean_pairs if p["level"] == "high")

    metadata = {
        "session_id": session_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "file_count": file_count,
        "highest_score": highest_score,
        "high_risk_pairs": high_risk_pairs,
    }

    (session_dir / METADATA_FILE).write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    (session_dir / ANALYSIS_FILE).write_text(
        json.dumps({"session_id": session_id, "pairs": clean_pairs}, indent=2),
        encoding="utf-8",
    )


def list_history() -> list[dict]:
    """
    Returns metadata for every session that has a saved analysis,
    newest first.
    """
    history: list[dict] = []

    if not UPLOAD_FOLDER.exists():
        return history

    for session_dir in UPLOAD_FOLDER.iterdir():
        if not session_dir.is_dir():
            continue
        metadata_path = session_dir / METADATA_FILE
        if not metadata_path.exists():
            continue
        try:
            history.append(json.loads(metadata_path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue

    history.sort(key=lambda item: item.get("created_at", ""), reverse=True)
    return history


def get_analysis(session_id: str) -> dict | None:
    """Returns the stored analysis ({session_id, pairs}) or None if missing."""
    analysis_path = UPLOAD_FOLDER / session_id / ANALYSIS_FILE
    if not analysis_path.exists():
        return None
    try:
        return json.loads(analysis_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def delete_session(session_id: str) -> bool:
    """Deletes the whole session folder. Returns True if it existed."""
    session_dir = (UPLOAD_FOLDER / session_id).resolve()

    # Safety: never delete anything outside the uploads folder.
    if UPLOAD_FOLDER.resolve() not in session_dir.parents:
        return False

    if not session_dir.exists() or not session_dir.is_dir():
        return False

    shutil.rmtree(session_dir)
    return True
