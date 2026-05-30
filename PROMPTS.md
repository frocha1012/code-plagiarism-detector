# Cursor Prompts

## Backend Structure

Given this project README, create a clean FastAPI architecture for a 5-day MVP.
Keep it modular but simple.

---

## Upload Endpoint

Create a FastAPI endpoint that:

* accepts multiple source code files
* validates file extensions
* stores files temporarily
* returns metadata

Allowed:
.py .java .cs .js

---

## Embeddings

Create a service using CodeBERT to generate embeddings from uploaded source code.

Requirements:

* reusable service
* batch processing
* clean code
* error handling

---

## Similarity

Implement cosine similarity between embeddings.

Return:

[
{
"file1": "",
"file2": "",
"score": 0.92
}
]

---

## React Results UI

Create a React component to display suspicious file pairs in a clean table.

Columns:

* file name
* compared file
* similarity %
* risk level
