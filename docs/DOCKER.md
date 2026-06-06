# Docker

Docker is provided for the **web version** only (backend + frontend). The
desktop (Tauri) build, Rust toolchain, Ollama, and any database are intentionally
left out — see the note at the bottom.

---

## Quick start

From the project root:

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000 (interactive docs at `/docs`)

Stop with `Ctrl+C`, or `docker compose down` to remove the containers.

---

## What runs

| Service | Build context | Port | Notes |
|---|---|---|---|
| `backend` | `./backend` | `8000` | FastAPI via Uvicorn. |
| `frontend` | `./frontend` | `5173` | React app built with Vite and served with `vite preview`. |

### Uploads volume

Uploaded files and session data are persisted on the host via a bind mount:

```yaml
volumes:
  - ./backend/uploads:/app/uploads
```

This means analyses survive container restarts and are visible on the host in
`backend/uploads/`.

### Frontend → backend

The frontend calls `http://localhost:8000/api`. Because the browser runs on the
host (not inside the container) and the backend publishes port `8000`, this
resolves correctly with no extra configuration.

---

## Ollama (optional, external)

Ollama is **not** containerized. AI explanations are optional — if Ollama is not
running, the app uses built-in fallback text.

To enable AI features, run Ollama on the host:

```bash
ollama pull llama3.1
ollama serve
```

The backend container reaches the host Ollama through `host.docker.internal`,
preconfigured in `docker-compose.yml`:

```yaml
environment:
  - OLLAMA_URL=http://host.docker.internal:11434/api/generate
extra_hosts:
  - "host.docker.internal:host-gateway"   # Linux compatibility
```

Override `OLLAMA_URL` if your Ollama instance runs elsewhere.

---

## Notes & expectations

- **First build is large/slow.** The backend installs `torch` + `transformers`
  (multi-gigabyte), and CodeBERT downloads on first run — this needs internet and
  some patience the first time.
- **Startup ordering.** `frontend` depends on `backend`, but `depends_on` waits
  for the container to start, not for Uvicorn to be fully ready. The very first
  request may arrive a moment early — just refresh.

> **Not dockerized on purpose:** Tauri, the Rust toolchain, Ollama, and any
> database. Docker here only covers the web version.
