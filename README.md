# Code Plagiarism Detector

A web and desktop application that detects similarities between source-code
files to support plagiarism review in an academic setting.

> **Projeto 4 — University Course Project**

---

## Overview

The Code Plagiarism Detector helps lecturers and teaching assistants identify
potentially copied source code among student submissions. Instead of relying on
plain text matching, it uses an AI code model (**CodeBERT**) to understand the
*meaning* of code, combined with a lexical overlap measure, to catch both
direct copies and disguised ones (e.g. renamed variables or reordered logic).

**Academic use case.** A reviewer uploads a batch of submissions (individual
files or a ZIP), the system compares every pair, ranks them by a similarity
score, and flags suspicious pairs by risk level. The reviewer can then inspect
matched lines side by side, request a natural-language explanation, export a PDF
report, and revisit past analyses from history.

**Workflow.**

1. **Upload** source files, a ZIP archive, or point at two public GitHub repos.
2. **Embed** each file into a 768-dimensional vector with CodeBERT.
3. **Score** every file pair using a hybrid semantic + lexical metric.
4. **Classify** each pair as High / Medium / Low risk.
5. **Review** matched lines, AI explanations, and an overall AI summary.
6. **Export** a PDF report and keep the analysis in history.

> Similarity scores are **indicators, not proof**. Final judgement always rests
> with a human reviewer.

---

## Features

- **File Upload** — upload multiple `.py`, `.java`, `.cs`, `.js` files.
- **ZIP Upload** — upload an archive; extracted safely (zip-slip protected).
- **GitHub Repository Comparison** — compare two public repositories directly.
- **CodeBERT Embeddings** — `microsoft/codebert-base`, mean-pooled, 768-dim.
- **Hybrid Similarity Scoring** — `0.7 × semantic (cosine) + 0.3 × lexical (Jaccard)`.
- **Risk Classification** — High / Medium / Low via configurable thresholds.
- **Compare View** — side-by-side matched lines, syntax-highlighted and grouped.
- **Ollama AI Explanations** — per-pair explanation via a local LLM (optional).
- **AI Summary** — a session-level natural-language summary (optional).
- **PDF Export** — downloadable report per analysis session (ReportLab).
- **Analysis History** — list, reopen, and delete past analyses.
- **Tauri Desktop Support** — run the same UI as a native desktop app.

AI features degrade gracefully: if Ollama is not running, the app returns
clear, data-driven fallback text instead of failing.

---

## Architecture

```text
React UI  (web via Vite  |  desktop via Tauri)
        │  HTTP (localhost:8000)
        ▼
FastAPI backend  (routes → services → utils)
        │
        ▼
CodeBERT embeddings  (HuggingFace Transformers)
        │
        ▼
Similarity engine  (hybrid: cosine + Jaccard, scikit-learn)
        │
        ├── Ollama (optional)  → AI explanations & summary
        └── ReportLab          → PDF reports
```

The React UI is identical between the web build (`npm run dev`) and the desktop
build (`npm run tauri:dev`); Tauri simply wraps the same frontend in a native
window. The backend always runs as a separate process.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for detail.

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 19, Vite, plain CSS (custom dark dashboard theme) |
| **Backend** | Python, FastAPI, Uvicorn, Pydantic |
| **AI / Embeddings** | HuggingFace Transformers, CodeBERT (`microsoft/codebert-base`), PyTorch |
| **Similarity** | scikit-learn, NumPy, hybrid cosine + Jaccard |
| **AI Explanations** | Ollama (`llama3.1`) — optional, local, with graceful fallback |
| **Reports** | ReportLab (in-memory PDF generation) |
| **Desktop** | Tauri 2 (Rust + WebView) |

---

## Similarity Methodology

Each file is converted into a numeric vector and compared with every other file.

1. **CodeBERT semantic similarity.** Every file is embedded into a 768-dim
   vector (mean pooling over token embeddings). The cosine similarity between
   two vectors captures *structural / semantic* closeness — it still scores high
   when identifiers are renamed or code is lightly reordered.

2. **Lexical similarity.** A token-level **Jaccard** overlap captures literal
   shared text (shared identifiers, string literals, comments).

3. **Hybrid score.** The final score blends both signals:

   ```text
   score = 0.7 × cosine(semantic) + 0.3 × jaccard(lexical)
   ```

   Semantic similarity dominates (catches disguised copies) while the lexical
   term grounds the score in concrete shared text.

4. **Risk thresholds** (configurable in `backend/app/config.py`):

   | Score | Risk | Interpretation |
   |---|---|---|
   | ≥ 85% | **High** | Strong suspicion — likely direct copy or renaming |
   | 78–84% | **Medium** | Structural overlap — manual review recommended |
   | < 78% | **Low** | Limited similarity — likely unrelated |

For matched-line inspection, the Compare View uses `difflib.SequenceMatcher`
above a separate line-match threshold.

---

## Installation

Requirements vary by option:

- **Docker:** Docker Desktop.
- **Manual:** Python 3.11+ and Node.js 18+.
- **Desktop:** the manual prerequisites plus the Rust toolchain and MSVC build
  tools (see [`docs/TAURI.md`](docs/TAURI.md)).

### Option A — Docker (web version)

```bash
docker compose up --build
```

### Option B — Manual setup

**Windows (helper scripts):**

```bat
setup.bat   :: creates venv, installs backend + frontend deps
```

**Manual / cross-platform:**

```bash
# Backend
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate    |    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### Option C — Tauri desktop

Install the Rust toolchain and C++ build tools, then `npm install` in
`frontend/`. Full steps in [`docs/TAURI.md`](docs/TAURI.md).

---

## Running the Project

| Target | Command | URL |
|---|---|---|
| **Backend** | `uvicorn app.main:app --reload --reload-dir app` (in `backend/`, venv active) | http://localhost:8000 (docs at `/docs`) |
| **Frontend** | `npm run dev` (in `frontend/`) | http://localhost:5173 |
| **Docker** | `docker compose up --build` | frontend `:5173`, backend `:8000` |
| **Tauri** | `npm run tauri:dev` (in `frontend/`) | native desktop window |

**Windows shortcuts:** `run.bat` (web) and `run_tauri.bat` (desktop) start
everything in one step.

### Ollama (optional, for AI features)

```bash
ollama pull llama3.1
ollama serve
```

If Ollama is not running, explanations and summaries fall back to clear,
data-driven text. For Docker, the backend reaches host Ollama via
`host.docker.internal` (preconfigured); override with the `OLLAMA_URL` env var.
See [`docs/DOCKER.md`](docs/DOCKER.md) for details.

---

## API Endpoints

Base path: `/api` (interactive docs at http://localhost:8000/docs).

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check. |
| `POST` | `/api/upload` | Upload code files or a ZIP; returns a `session_id`. |
| `POST` | `/api/analyze?session_id=` | Embed + score all file pairs for a session. |
| `GET` | `/api/files/{session_id}/{filename}` | Return stored source for one file. |
| `GET` | `/api/compare/{session_id}?file1=&file2=` | Matched similar lines between two files. |
| `POST` | `/api/explain` | AI explanation for one pair (Ollama, with fallback). |
| `POST` | `/api/summary` | AI session-level summary (Ollama, with fallback). |
| `GET` | `/api/report/{session_id}` | Download a PDF report for the session. |
| `GET` | `/api/history` | List all saved analyses (newest first). |
| `GET` | `/api/history/{session_id}` | Reopen a stored analysis. |
| `DELETE` | `/api/history/{session_id}` | Delete a session and its files. |
| `POST` | `/api/github/compare` | Compare two public GitHub repositories. |
| `GET` | `/api/meta` | Similarity thresholds + project statistics. |

---

## Project Structure

```text
P4/
├── backend/            FastAPI service
│   ├── app/
│   │   ├── routes/     thin HTTP endpoints
│   │   ├── services/   business logic (embedding, similarity, explain, report, github, history, upload)
│   │   ├── utils/      file + line-comparison helpers
│   │   ├── models/     Pydantic schemas
│   │   ├── config.py   thresholds, paths, CORS, Ollama config
│   │   └── main.py     app entry + router registration
│   ├── tests/          test + sample fixtures (small, large, 12-file batch)
│   └── uploads/        per-session uploaded files (runtime)
├── frontend/           React + Vite UI (also builds the Tauri desktop app)
│   ├── src/            components, pages, services/api.js
│   └── src-tauri/      Tauri desktop wrapper
├── docs/               architecture, docker, tauri, screenshots
├── docker-compose.yml  runs backend + frontend (web)
└── *.bat               Windows helper scripts
```

- **`routes/` stay thin** — they validate input and delegate to `services/`.
- **`services/`** hold all logic; **`utils/`** hold small reusable helpers.

---

## Screenshots

> Place images in `docs/screenshots/` and reference them here.

| View | Preview |
|---|---|
| Upload page | `![Upload](docs/screenshots/upload.png)` |
| Results dashboard | `![Results](docs/screenshots/results.png)` |
| Compare view | `![Compare](docs/screenshots/compare.png)` |
| AI explanation | `![Explain](docs/screenshots/explain.png)` |

---

## Limitations

- **Indicators, not proof.** A high score signals *similarity*, not guilt; every
  flagged pair needs human review before any academic decision.
- **Common patterns inflate scores.** Shared starter code, boilerplate, common
  algorithms, or the same tutorial can legitimately produce high similarity.
- **Small files are unreliable.** Very short files have little signal, so scores
  are noisier and less meaningful.
- **Language coverage.** Limited to `.py`, `.java`, `.cs`, `.js`.
- **No cross-language detection** and **no AST-level analysis** (textual/semantic
  embeddings only).

---

## Future Work

- AST-based structural detection (beyond textual/embedding similarity).
- Cross-language similarity detection.
- Stronger identifier/structure normalization.
- FAISS vector index for large submission sets.
- Multi-session batch analysis and a richer teacher dashboard.
- Optional Ollama model selection in the UI.

---

## Authors

- **Fernando Rocha** — Student — [fernandorocha@ipvc.pt](mailto:fernandorocha@ipvc.pt)

> **Course:** LEI — Projeto 4 (P4)   |   **Institution:** IPVC   |   **Year:** 2026
