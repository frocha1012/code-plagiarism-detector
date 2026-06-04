"""
GitHub repository comparison.

This is just another *input source* for the existing plagiarism pipeline:
it downloads two public repositories as ZIP archives, extracts their source
files into a normal upload session (one sub-folder per repository), then hands
the session straight to the unchanged embedding + similarity + history flow.

Nothing about CodeBERT embeddings, hybrid scoring, Ollama, Compare View,
PDF export, or History is touched here.

Download strategy:
    1. Try the GitHub API zipball endpoint (resolves the default branch).
    2. Fall back to the codeload archive for ``main`` then ``master``.
    No ``git clone`` and no extra dependencies — uses urllib from the stdlib.
"""

import io
import json
import re
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from app.config import (
    ALLOWED_EXTENSIONS,
    GITHUB_IGNORED_DIRS,
    GITHUB_MAX_DOWNLOAD_SIZE,
    GITHUB_MAX_FILES_PER_REPO,
    GITHUB_REQUEST_TIMEOUT,
    MAX_FILE_SIZE,
    UPLOAD_FOLDER,
)
from app.services.embedding_service import generate_embeddings
from app.services.history_service import save_analysis
from app.services.similarity_service import compute_similarity
from app.utils.file_utils import (
    SOURCE_FILE,
    get_session_dir,
    list_session_files,
    new_session_id,
    read_file,
)

_USER_AGENT = "code-plagiarism-detector"
_GITHUB_URL_RE = re.compile(
    r"^(?:https?://)?(?:www\.)?github\.com/([^/\s]+)/([^/\s#?]+)",
    re.IGNORECASE,
)


# ── URL parsing ───────────────────────────────────────────────────────────────

def parse_repo(url: str) -> tuple[str, str]:
    """Extracts (owner, repo) from a GitHub URL.

    Accepts forms like:
        https://github.com/user/project
        https://github.com/user/project.git
        github.com/user/project/tree/main
    Raises ValueError for anything that is not a GitHub repository URL.
    """
    match = _GITHUB_URL_RE.match((url or "").strip())
    if not match:
        raise ValueError("Invalid GitHub repository URL.")

    owner = match.group(1)
    repo = match.group(2)
    if repo.endswith(".git"):
        repo = repo[: -len(".git")]

    if not owner or not repo:
        raise ValueError("Invalid GitHub repository URL.")

    return owner, repo


# ── Download ──────────────────────────────────────────────────────────────────

def _fetch(url: str) -> bytes:
    """Downloads a URL, enforcing the maximum archive size while streaming."""
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(request, timeout=GITHUB_REQUEST_TIMEOUT) as response:
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = response.read(64 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > GITHUB_MAX_DOWNLOAD_SIZE:
                raise ValueError("Repository exceeds analysis limits.")
            chunks.append(chunk)
    return b"".join(chunks)


def download_repo_zip(owner: str, repo: str) -> bytes:
    """Downloads a repository as a ZIP archive.

    Tries the API zipball (default branch) first, then the main/master
    codeload archives. Raises ValueError with a user-friendly message if the
    repository cannot be downloaded.
    """
    candidate_urls = [
        f"https://api.github.com/repos/{owner}/{repo}/zipball",
        f"https://codeload.github.com/{owner}/{repo}/zip/refs/heads/main",
        f"https://codeload.github.com/{owner}/{repo}/zip/refs/heads/master",
    ]

    last_error: Exception | None = None
    for url in candidate_urls:
        try:
            return _fetch(url)
        except ValueError:
            # Size limit hit — surface immediately, retrying won't help.
            raise
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            continue

    raise ValueError("Repository could not be downloaded.") from last_error


# ── Safe extraction ─────────────────────────────────────────────────────────--

def _should_skip(rel_parts: tuple[str, ...]) -> bool:
    """True if any directory in the path is on the ignore list or hidden."""
    for part in rel_parts[:-1]:
        if part in GITHUB_IGNORED_DIRS or part.startswith("."):
            return True
    return False


def extract_repo(zip_bytes: bytes, session_id: str, repo_label: str) -> int:
    """Extracts supported source files from a repo ZIP into the session folder.

    Files are stored under ``<session>/<repo_label>/<original/sub/path>`` so
    results clearly show which repository each file came from.

    Safety rules:
      - Strips the archive's top-level ``<repo>-<ref>/`` folder.
      - Skips ignored directories, hidden files, and non-source extensions.
      - Skips files larger than MAX_FILE_SIZE.
      - Enforces GITHUB_MAX_FILES_PER_REPO.
      - Verifies every resolved destination stays inside the repo folder
        (zip-slip / path-traversal prevention).

    Returns the number of source files saved.
    """
    session_dir = get_session_dir(session_id)
    repo_root = (session_dir / repo_label).resolve()
    repo_root.mkdir(parents=True, exist_ok=True)

    saved = 0
    try:
        archive = zipfile.ZipFile(io.BytesIO(zip_bytes))
    except zipfile.BadZipFile as exc:
        raise ValueError("Repository could not be downloaded.") from exc

    with archive as zf:
        for entry in zf.infolist():
            if entry.is_dir():
                continue

            parts = Path(entry.filename).parts
            if len(parts) <= 1:
                continue  # the archive root itself; real content lives one level down

            rel_parts = parts[1:]  # drop "<repo>-<ref>/"
            if _should_skip(rel_parts):
                continue

            name = rel_parts[-1]
            if name.startswith("."):
                continue
            if Path(name).suffix.lower() not in ALLOWED_EXTENSIONS:
                continue
            if entry.file_size > MAX_FILE_SIZE:
                continue

            if saved >= GITHUB_MAX_FILES_PER_REPO:
                raise ValueError("Repository exceeds analysis limits.")

            destination = (repo_root / Path(*rel_parts)).resolve()
            # Zip-slip: destination must stay inside the repo folder.
            if repo_root not in destination.parents:
                continue

            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(zf.read(entry.filename))
            saved += 1

    return saved


# ── Orchestration ──────────────────────────────────────────────────────────--

def _unique_labels(repo_1: str, repo_2: str) -> tuple[str, str]:
    """Folder labels for each repo; disambiguated if both names match."""
    if repo_1.lower() == repo_2.lower():
        return f"{repo_1}-1", f"{repo_2}-2"
    return repo_1, repo_2


def compare_repositories(repo_url_1: str, repo_url_2: str) -> dict:
    """Downloads two repositories and runs the existing similarity pipeline.

    Returns {"session_id": str, "pairs": [...]} — identical in shape to the
    normal /analyze endpoint. Results are persisted to History automatically.
    """
    owner_1, repo_1 = parse_repo(repo_url_1)
    owner_2, repo_2 = parse_repo(repo_url_2)

    label_1, label_2 = _unique_labels(repo_1, repo_2)
    session_id = new_session_id()
    get_session_dir(session_id)  # create the folder up-front

    zip_1 = download_repo_zip(owner_1, repo_1)
    count_1 = extract_repo(zip_1, session_id, label_1)

    zip_2 = download_repo_zip(owner_2, repo_2)
    count_2 = extract_repo(zip_2, session_id, label_2)

    if count_1 == 0 and count_2 == 0:
        raise ValueError("No supported source files were found.")

    session_dir = UPLOAD_FOLDER / session_id

    # Build the analysis set: repo-prefixed relative paths ("project-a/main.py"),
    # skipping empty / whitespace-only files. Blank files (e.g. __init__.py)
    # otherwise score 100% against each other and just add noise.
    analyzed_1 = analyzed_2 = 0
    filenames: list[str] = []
    snippets: list[str] = []
    for path in list_session_files(session_id):
        content = read_file(path)
        if not content.strip():
            continue
        rel = path.relative_to(session_dir).as_posix()
        filenames.append(rel)
        snippets.append(content)
        if rel.split("/", 1)[0] == label_1:
            analyzed_1 += 1
        else:
            analyzed_2 += 1

    # A meaningful comparison needs at least one non-empty file from each repo.
    if analyzed_1 == 0 or analyzed_2 == 0:
        raise ValueError("No supported source files were found.")

    embeddings = generate_embeddings(snippets)
    all_pairs = compute_similarity(filenames, embeddings, snippets)

    # Cross-repo only: this feature compares repo A against repo B, never a
    # repository against itself.
    pairs = [
        pair
        for pair in all_pairs
        if pair["file1"].split("/", 1)[0] != pair["file2"].split("/", 1)[0]
    ]

    # Persist download info alongside metadata/analysis written by save_analysis.
    download_info = {
        "source": "github",
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "repositories": [
            {
                "url": repo_url_1,
                "owner": owner_1,
                "repo": repo_1,
                "label": label_1,
                "file_count": count_1,
                "analyzed_file_count": analyzed_1,
            },
            {
                "url": repo_url_2,
                "owner": owner_2,
                "repo": repo_2,
                "label": label_2,
                "file_count": count_2,
                "analyzed_file_count": analyzed_2,
            },
        ],
    }
    (session_dir / SOURCE_FILE).write_text(
        json.dumps(download_info, indent=2), encoding="utf-8"
    )

    save_analysis(session_id, pairs)

    return {"session_id": session_id, "pairs": pairs}
