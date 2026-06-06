# Architecture

This document describes how the Code Plagiarism Detector is structured and how a
request flows through the system.

---

## High-level overview

```text
React UI  (web via Vite  |  desktop via Tauri)
        │  HTTP (localhost:8000)
        ▼
FastAPI backend
   routes/  →  services/  →  utils/
        │
        ▼
CodeBERT embeddings  (HuggingFace Transformers + PyTorch)
        │
        ▼
Similarity engine  (hybrid cosine + Jaccard, scikit-learn / NumPy)
        │
        ├── Ollama (optional)  → AI explanations & summary
        └── ReportLab          → PDF reports
```

The frontend is a single React app. The same source builds both the **web**
version (served by Vite) and the **desktop** version (wrapped by Tauri). In both
cases the UI talks to the backend over plain HTTP at `http://localhost:8000`.

The backend is a FastAPI service organized into four layers.

---

## Backend layers

| Layer | Folder | Responsibility |
|---|---|---|
| **Routes** | `backend/app/routes/` | Define HTTP endpoints, validate input, translate errors to HTTP status codes, and delegate to services. They contain no business logic. |
| **Services** | `backend/app/services/` | All business logic: embeddings, similarity, explanations, reports, GitHub download, history, upload handling. |
| **Utils** | `backend/app/utils/` | Small reusable helpers: safe file access and line-by-line comparison. |
| **Models** | `backend/app/models/` | Pydantic schemas shared across routes/services. |

Configuration (thresholds, paths, CORS origins, Ollama settings) is centralized
in `backend/app/config.py`.

### Services at a glance

- **`upload_service`** — validates and stores uploaded files (and ZIPs) under a
  unique `uploads/<session_id>/` folder. Enforces extension and size limits and
  prevents zip-slip path traversal.
- **`embedding_service`** — lazily loads CodeBERT once, then generates a
  768-dimensional vector per file (mean pooling).
- **`similarity_service`** — computes the hybrid score for every file pair and
  assigns a risk level.
- **`github_service`** — downloads two public repositories as ZIP archives,
  extracts supported source files into a session, and reuses the normal
  embedding + similarity pipeline.
- **`explain_service`** — builds prompts and calls a local Ollama instance for
  per-pair explanations and session summaries, with graceful fallbacks.
- **`report_service`** — renders a PDF report for a session with ReportLab.
- **`history_service`** — persists analysis metadata/results so sessions can be
  listed, reopened, and deleted, and exposes aggregate statistics.

---

## Request flow: upload → analyze

```text
1. POST /api/upload        upload_service stores files, returns session_id
2. POST /api/analyze       list session files
                           → embedding_service.generate_embeddings()
                           → similarity_service.compute_similarity()
                           → history_service.save_analysis()
                           → returns ranked pairs with risk levels
3. GET  /api/compare/...   utils.find_similar_lines() for two files
4. POST /api/explain       explain_service → Ollama (or fallback)
5. POST /api/summary       explain_service → Ollama (or fallback)
6. GET  /api/report/...    report_service → PDF
```

The GitHub flow (`POST /api/github/compare`) replaces step 1–2: it downloads and
extracts repositories, then runs the same embedding + similarity + history path
and returns the same response shape as `/api/analyze`.

---

## Similarity scoring

```text
score = 0.7 × cosine(CodeBERT embeddings) + 0.3 × jaccard(token overlap)
```

- The **semantic** term (CodeBERT cosine) captures structural meaning and stays
  high under variable/function renaming or light reordering.
- The **lexical** term (Jaccard over tokens) grounds the score in literal shared
  text.
- Pairs are classified using thresholds in `config.py`
  (High ≥ 85%, Medium ≥ 78%, otherwise Low).

Matched-line inspection in the Compare View uses `difflib.SequenceMatcher` above
a separate line-match threshold.

---

## Optional AI (Ollama)

AI explanations and summaries are **optional**. The backend calls a local Ollama
server; every failure mode (offline, timeout, bad response) is caught and the
service returns a deterministic, data-driven fallback. As a result the API never
fails because of AI, and the UI renders fallback text the same way it renders a
real response.
