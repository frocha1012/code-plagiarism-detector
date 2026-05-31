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

# Create upload folder automatically
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)