# TODO — Projeto 4

## Core Features — ✅ COMPLETE

### Backend
* [x] FastAPI app with CORS, modular routers, Pydantic schemas
* [x] File upload endpoint (POST /api/upload)
* [x] Session-based upload storage
* [x] File extension validation (.py, .java, .cs, .js)
* [x] ZIP archive upload with safe extraction (zip-slip prevention)
* [x] CodeBERT embeddings (microsoft/codebert-base, mean pooling, 768-dim)
* [x] Hybrid similarity scoring (0.7 × semantic cosine + 0.3 × lexical Jaccard)
* [x] Similarity analysis endpoint (POST /api/analyze)
* [x] Risk level labels (high / medium / low) with configurable thresholds
* [x] Line-by-line compare endpoint (GET /api/compare/{session_id})
* [x] File content endpoint (GET /api/files/{session_id}/{filename})
* [x] PDF report export (GET /api/report/{session_id})
* [x] Ollama AI explanation endpoint (POST /api/explain) with graceful fallback

### Frontend
* [x] React + Vite setup
* [x] Upload page with dropzone (multiple files or ZIP)
* [x] Animated analysis loading screen with progress ring and step list
* [x] Results page with summary metrics (files, suspicious pairs, highest score)
* [x] Similarity cards with risk-level styling
* [x] Compare Files button (high + medium only)
* [x] Similar Code Lines viewer (syntax highlighted, grouped consecutive lines)
* [x] Explain with AI button with loading spinner and bullet-list rendering
* [x] Export PDF Report button
* [x] Low-risk pairs show "No significant similarities detected"
* [x] Modern dark dashboard UI

### Testing
* [x] Small sample files: original, renamed, unrelated
* [x] Large files: library management, inventory (original + renamed + partial)
* [x] Truly unrelated files: matrix simulation, recipe planner
* [x] Fallback behavior when Ollama is offline

---

## Remaining

### Nice-to-have
* [ ] Strip stray intro lines from Ollama bullet output
* [ ] Format fallback explanation as a bullet for visual consistency
* [ ] Timeout hint near AI spinner

---

## Not Doing (for this project)
* Docker
* FAISS
* Tauri desktop app
* Authentication
* Database
* AST-based detection
* Cross-language similarity
