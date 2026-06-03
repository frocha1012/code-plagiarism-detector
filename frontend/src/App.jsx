import { useState } from "react";
import UploadPage from "./pages/UploadPage";
import ResultsPage from "./pages/ResultsPage";
import HistoryPage from "./pages/HistoryPage";

export default function App() {
  const [view, setView] = useState("upload"); // "upload" | "results" | "history"
  const [analysisResult, setAnalysisResult] = useState(null);

  function showResults(result) {
    setAnalysisResult(result);
    setView("results");
  }

  function goHome() {
    setAnalysisResult(null);
    setView("upload");
  }

  return (
    <div className="app-shell">
      <div className="app-content">
        <header className="app-nav">
          <button className="app-brand" type="button" onClick={goHome}>
            <span className="app-brand-mark" aria-hidden="true">
              &lt;/&gt;
            </span>
            <span>Plagiarism Detector</span>
          </button>
          <nav className="app-nav-links">
            <button
              type="button"
              className={`nav-link ${view !== "history" ? "active" : ""}`}
              onClick={goHome}
            >
              Home
            </button>
            <button
              type="button"
              className={`nav-link ${view === "history" ? "active" : ""}`}
              onClick={() => setView("history")}
            >
              History
            </button>
          </nav>
        </header>

        <main className="app-main">
          {view === "upload" && <UploadPage onResults={showResults} />}
          {view === "results" && analysisResult && (
            <ResultsPage results={analysisResult} onReset={goHome} />
          )}
          {view === "history" && <HistoryPage onOpen={showResults} />}
        </main>
      </div>
    </div>
  );
}
