# Commands — Projeto 4
Quick reference for running the full stack locally.

---

## 1. Backend

### First time only — create virtual environment

```powershell
cd C:\Users\froch\Desktop\P4\backend
python -m venv .venv
```

### Activate virtual environment

```powershell
cd C:\Users\froch\Desktop\P4\backend
.venv\Scripts\Activate.ps1
```

> If PowerShell blocks script execution, run once:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### First time only — install dependencies

```powershell
pip install -r requirements.txt
```

### Run the backend server

```powershell
uvicorn app.main:app --reload --reload-dir app
```

Backend runs at: http://localhost:8000
Swagger docs at: http://localhost:8000/docs

---

## 2. Frontend

Open a **new** terminal tab/window.

### First time only — install dependencies

```powershell
cd C:\Users\froch\Desktop\P4\frontend
npm install
```

### Run the dev server

```powershell
cd C:\Users\froch\Desktop\P4\frontend
npm run dev
```

Frontend runs at: http://localhost:5173

---

## 3. Ollama (optional — AI explanations & summary)

Ollama must be running for the "Explain with AI" and "Generate AI Summary" buttons to work.
If it is not running, both features return a graceful fallback message automatically.

### First time only — pull the model

```powershell
ollama pull llama3.1
```

### Start Ollama server

```powershell
ollama serve
```

> If you get "port already in use", Ollama is already running in the background — skip this step.

Ollama runs at: http://localhost:11434

---

## 4. Full startup order

1. Activate venv + start backend
2. Start frontend dev server
3. (Optional) Start Ollama

---

## 5. Stop everything

- Backend: `Ctrl+C` in the backend terminal
- Frontend: `Ctrl+C` in the frontend terminal
- Ollama: `Ctrl+C` in the Ollama terminal (or leave it running)
