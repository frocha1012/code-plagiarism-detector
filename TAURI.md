# Tauri Desktop App — Setup Guide
**Projeto 4**

The React frontend can run as a native Windows desktop app using Tauri.
The FastAPI backend remains a separate process — Tauri just wraps the web UI.

---

## Prerequisites

### 1. Install Rust

Tauri requires the Rust toolchain. Install it from:
https://rustup.rs

Run the installer and follow the instructions. After installing, open a new terminal and verify:

```powershell
rustc --version
cargo --version
```

### 2. Install Visual Studio C++ Build Tools (Windows)

Rust on Windows needs the MSVC build tools. If you don't have them:

- Download **Visual Studio Build Tools** from:
  https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Select **"Desktop development with C++"** and install.

### 3. Install Node.js dependencies (including Tauri CLI)

```powershell
cd C:\Users\froch\Desktop\P4\frontend
npm install
```

This installs `@tauri-apps/cli` automatically.

### 4. Generate app icons (one time only)

Tauri requires icon files in `src-tauri/icons/`. Generate them from any 1024×1024 PNG:

```powershell
cd C:\Users\froch\Desktop\P4\frontend
npx tauri icon path/to/your-icon.png
```

This creates all required icon sizes automatically.

---

## Running the Desktop App

### Step 1 — Start the backend

```powershell
cd C:\Users\froch\Desktop\P4\backend
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --reload-dir app
```

Backend must be running at http://localhost:8000 before launching the desktop app.

### Step 2 — Start Ollama (optional)

```powershell
ollama serve
```

### Step 3 — Launch the Tauri desktop app

```powershell
cd C:\Users\froch\Desktop\P4\frontend
npm run tauri:dev
```

This starts the Vite dev server and opens a native desktop window showing the React app.
The app calls the backend at http://localhost:8000 exactly as the web version does.

---

## Building a Distributable Desktop App

```powershell
cd C:\Users\froch\Desktop\P4\frontend
npm run tauri:build
```

Output is placed in `frontend/src-tauri/target/release/bundle/`.

---

## Architecture Note

```
Desktop Window (Tauri/WebView)
        ↓
React UI (same as web version)
        ↓
HTTP calls to http://localhost:8000
        ↓
FastAPI Backend (separate process)
```

The React UI is identical between the web version (`npm run dev`) and the desktop version (`npm run tauri:dev`).
No components were modified. The backend is always a separate process.

---

## Web version still works

The existing web version is unaffected:

```powershell
npm run dev    # web version at http://localhost:5173
npm run tauri:dev    # desktop version as a native window
```
