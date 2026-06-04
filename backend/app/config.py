from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Storage
UPLOAD_FOLDER = BASE_DIR / "uploads"

# File validation
ALLOWED_EXTENSIONS = {
    ".py",
    ".java",
    ".cs",
    ".js",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# CORS
CORS_ORIGINS = [
    "http://localhost:5173",
]

# Similarity thresholds
HIGH_SIMILARITY_THRESHOLD = 0.85
MEDIUM_SIMILARITY_THRESHOLD = 0.78

# Compare view
LINE_MATCH_SIMILARITY_THRESHOLD = 0.75

# Ollama (optional AI explanations)
OLLAMA_MODEL = "llama3.1"
OLLAMA_URL = "http://localhost:11434/api/generate"

# GitHub repository comparison
GITHUB_MAX_FILES_PER_REPO = 100
GITHUB_MAX_DOWNLOAD_SIZE = 60 * 1024 * 1024  # 60 MB per repo archive
GITHUB_REQUEST_TIMEOUT = 30  # seconds
GITHUB_IGNORED_DIRS = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "target",
    ".next",
    "coverage",
}

# Create upload folder automatically
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)