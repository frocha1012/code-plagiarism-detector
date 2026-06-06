# Project Rules

## Goal

Finish a working MVP in 5 days.

This project prioritizes:

1. Functionality
2. Simplicity
3. Demo readiness

NOT optimization or enterprise architecture.

---

## Tech Constraints

### Backend

* FastAPI only
* Modular but simple
* No unnecessary abstractions
* No microservices

### Frontend

* React + Vite
* Simple UI
* Functional over pretty

### AI

* CodeBERT for embeddings
* Cosine similarity for comparison
* Ollama only if time allows

---

## Architecture Rules

Always use:

routes/
services/
models/
utils/

Keep logic separated.

Example:

* routes = API endpoints
* services = business logic
* utils = helpers

---

## Important Constraints

DO NOT:

* Overengineer
* Create unnecessary design patterns
* Add authentication
* Add databases unless necessary
* Add Docker unless required
* Add FAISS before MVP works

DO:

* Build incrementally
* Test after each feature
* Keep code readable
* Prefer working code over perfect code

---

## MVP Definition

The MVP is complete when:

* User uploads multiple files
* Embeddings are generated
* Similarity is calculated
* Suspicious pairs are shown
* Side-by-side comparison works

Anything else is optional.

---

## Development Philosophy

Always implement the smallest working version first.

Bad:
“Build enterprise plagiarism detection architecture.”

Good:
“Build upload → compare → display.”
