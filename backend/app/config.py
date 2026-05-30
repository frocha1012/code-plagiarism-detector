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

# Similarity thresholds (used later)
HIGH_SIMILARITY_THRESHOLD = 0.90
MEDIUM_SIMILARITY_THRESHOLD = 0.75

# Create upload folder automatically
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)