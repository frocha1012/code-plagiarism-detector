# Code Plagiarism Detector
**Projeto 4 — University Course Project**

---

## Project Goal

Build a web application capable of detecting similarities between source code files to identify potential plagiarism in an academic context.

The system compares uploaded source code files using **AI embeddings specialized for code understanding** and calculates similarity scores between all pairs. It can optionally generate a natural-language explanation of the detected similarity using a **local LLM (Ollama)**.

The application detects:

* Direct code copies
* Variable and function renaming
* Formatting modifications
* Minor logical restructuring
* Structural similarity

---

## Tech Stack

### Frontend

* React + Vite
* Plain CSS (custom dark dashboard theme)

### Backend

* Python
* FastAPI

### AI / Embeddings

* HuggingFace Transformers
* CodeBERT (`microsoft/codebert-base`)

### Similarity

* Hybrid scoring: 0.7 × semantic (cosine) + 0.3 × lexical (Jaccard)
* scikit-learn

### AI Explanations

* Ollama (llama3.1) — optional, graceful fallback if offline

---

## Architecture

```text
Frontend (React + Vite)
        ↓
FastAPI Backend
        ↓
File Upload & Session Management
        ↓
CodeBERT Embedding Generation
        ↓
Hybrid Similarity Scoring
        ↓
Results + Line Comparison + AI Explanation
```

---

## Features

### Core

* [x] Upload multiple code files or a single ZIP archive
* [x] Support for Python, Java, C#, JavaScript
* [x] CodeBERT embeddings (mean pooling, 768-dimensional)
* [x] Hybrid similarity scoring (semantic + lexical)
* [x] Pairwise comparison across all uploaded files
* [x] Risk level classification: High / Medium / Low
* [x] Similarity results dashboard with score cards
* [x] Similar Code Lines viewer (syntax highlighted, grouped blocks)
* [x] Ollama AI explanation per pair (4 structured bullets, offline fallback)
* [x] PDF report export (session-based, ReportLab)
* [x] Animated analysis screen with progress ring

### Security

* [x] File extension validation
* [x] Max file size enforcement
* [x] ZIP extraction path traversal prevention (zip-slip)
* [x] Session-scoped file access only

---

## Similarity Thresholds

| Score | Risk Level | Interpretation |
|---|---|---|
| ≥ 85% | High | Strong suspicion — likely renaming or direct copy |
| 78–84% | Medium | Structural overlap — manual review recommended |
| < 78% | Low | Limited similarity — likely unrelated |

Thresholds are configurable in `backend/app/config.py`.

---

## Folder Structure

```text
P4/
├── backend/
│   ├── app/
│   │   ├── routes/         # upload, similarity, compare, report, explain
│   │   ├── services/       # upload, embedding, similarity, report, explain
│   │   ├── utils/          # file_utils, compare_utils
│   │   ├── models/         # Pydantic schemas
│   │   ├── config.py
│   │   └── main.py
│   ├── tests/
│   │   └── sample_files/   # test fixtures (small + big_batch)
│   ├── uploads/            # session folders (git-ignored)
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/     # SimilarityTable, CompareView, AnalysisLoader
│   │   ├── pages/          # UploadPage, ResultsPage
│   │   ├── services/       # api.js
│   │   └── App.jsx
│
├── development_status/     # audit and progress notes
├── README.md
└── TODO.md
```

---

## Development Rules

* Keep backend modular — routes stay thin, logic lives in services
* No unnecessary abstractions
* Avoid overengineering
* Build incrementally, test after every major feature
* Prefer readability over optimization

---

## Success Criteria

* A user can upload multiple source code files or a ZIP archive
* The system generates similarity scores for all pairs
* Suspicious pairs are identified and labeled with a risk level
* Similar code lines are shown with syntax highlighting
* An AI explanation can be requested per pair
* A PDF report can be exported
* The application is demo-ready

---

## Future Improvements

* AST-based plagiarism detection (structural, not textual)
* Cross-language similarity detection
* More advanced code normalization (identifier abstraction)
* Teacher dashboard with session history
* Batch analysis across many sessions
* Desktop app using Tauri
* Docker deployment
* FAISS vector index for large submission sets
