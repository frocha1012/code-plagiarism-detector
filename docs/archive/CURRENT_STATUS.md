# Current Status
**Last updated:** 2026-05-31

## Completed

### Backend
- FastAPI app with CORS, modular routers, Pydantic schemas
- File upload with session storage, extension validation, max size check
- ZIP archive upload with safe extraction (zip-slip prevention, __MACOSX filtering)
- CodeBERT embeddings (microsoft/codebert-base, mean pooling, 768-dim)
- Hybrid similarity scoring (0.7 × semantic cosine + 0.3 × lexical Jaccard)
- Risk level thresholds: HIGH ≥ 0.85, MEDIUM ≥ 0.78
- Line-by-line comparison (difflib SequenceMatcher, configurable threshold)
- PDF report export (ReportLab, in-memory generation)
- Ollama AI explanation (POST /api/explain, llama3.1, graceful fallback if offline)

### Frontend
- Dark AI/SaaS dashboard UI (plain CSS, glassmorphism, no UI library)
- Upload page with dropzone, ZIP support, animated analysis loader
- Results page with summary cards, risk-level result cards
- Compare Files view (syntax-highlighted, grouped consecutive lines)
- Explain with AI button (bullets, loading spinner, result caching)
- Export PDF Report button
- Low-risk pairs show informational note instead of compare/explain actions

### Testing & Fixtures
- sample_files/: original.py, renamed_variables.py, unrelated.py
- sample_files/: large_original.py, large_renamed.py, large_unrelated.py
- sample_files/big_batch/: 12 files (300 lines each) covering high/medium/low scenarios

## In Progress
- Ollama output post-processing (strip stray intro lines from bullets)

## Known Issues
- Ollama may prepend an intro sentence before bullets → renders as extra bullet item
- Fallback explanation is plain prose, not bullet-formatted (minor visual inconsistency)

## Not Doing
- Docker, FAISS, Tauri, authentication, database, AST detection
