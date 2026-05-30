# Code Plagiarism Detector using Embeddings and Local LLM

## Project Goal

Build an application capable of detecting similarities between source code files to identify potential plagiarism in an academic context.

The system will compare uploaded source code files using **AI embeddings specialized for code understanding** and calculate similarity scores between them.

The application should detect:

* Direct code copies
* Variable/function renaming
* Formatting modifications
* Minor logical restructuring

The system may optionally generate an explanation of the detected similarity using a **local LLM (Ollama)**.

---

## Project Scope (5-Day MVP)

### Goal for MVP

A working web application where the user can:

1. Upload multiple code files
2. Generate embeddings for each file
3. Compare files using cosine similarity
4. View suspicious similarity pairs
5. Open a side-by-side comparison

This MVP must be **functional first, polished second**.

---

## Tech Stack

### Frontend

* React
* Vite
* Tailwind CSS (optional)

### Backend

* Python
* FastAPI

### AI / Embeddings

* HuggingFace Transformers
* CodeBERT

### Similarity

* Cosine Similarity
* scikit-learn

### Optional (Only if time allows)

* Ollama for explanations
* FAISS for vector indexing

---

## Architecture

```text
Frontend (React)
        ↓
FastAPI Backend
        ↓
Code Processing Layer
        ↓
CodeBERT Embeddings
        ↓
Cosine Similarity Analysis
        ↓
Similarity Results
```

---

## Features

### MVP Features (Required)

* [ ] Upload multiple code files

* [ ] Support common programming languages

  * Python
  * Java
  * C#
  * JavaScript

* [ ] Generate embeddings from source code

* [ ] Compare all uploaded files

* [ ] Calculate cosine similarity score

* [ ] Display suspicious file pairs

* [ ] Similarity matrix/table

* [ ] Side-by-side file comparison

---

### Optional Features (Stretch Goals)

* [ ] Ollama similarity explanation
* [ ] Highlight suspicious code regions
* [ ] Export PDF report
* [ ] Better UI styling
* [ ] Drag & drop upload

---

## Similarity Rules

Suggested thresholds:

* **90%+** → High plagiarism suspicion
* **75–89%** → Medium suspicion
* **Below 75%** → Low suspicion

These thresholds may be adjusted after testing.

---

## Folder Structure

```text
project-root/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── uploads/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│
├── docs/
│
├── README.md
└── TODO.md
```

---

## Development Plan (5 Days)

### Day 1

* Setup project structure
* Setup FastAPI backend
* Setup React frontend
* Implement file upload

### Day 2

* Integrate CodeBERT
* Generate embeddings from uploaded code
* Test embedding generation

### Day 3

* Implement cosine similarity
* Compare uploaded files
* Return similarity results

### Day 4

* Create frontend results view
* Build similarity table
* Build side-by-side comparison view

### Day 5

* Bug fixing
* UI improvements
* Optional Ollama integration
* Prepare demo screenshots

---

## Development Rules

### Important Project Rules

* Keep backend modular
* Prefer simple implementations first
* Do not overengineer
* Prioritize a working MVP
* Avoid unnecessary complexity
* Build features incrementally
* Test after every major feature

### AI Assistant Instructions (Cursor Context)

When generating code:

* Use clean architecture
* Keep components modular
* Avoid unnecessary abstractions
* Explain important implementation decisions
* Prefer readability over optimization
* Focus on MVP completion within 5 days

---

## Success Criteria

The project is considered successful if:

* A user can upload multiple source code files
* The system generates similarity scores
* Suspicious pairs are identified
* The UI displays comparison results clearly
* The application is demo-ready

---

## Future Improvements

* AST-based plagiarism detection
* Cross-language similarity detection
* More advanced code normalization
* Teacher dashboard
* Batch analysis
* PDF report generation
* Desktop app using Tauri
