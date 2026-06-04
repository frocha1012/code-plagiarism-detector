import { useEffect, useState } from "react";
import AnalysisLoader from "../components/AnalysisLoader";
import { uploadFiles, analyzeFiles, compareGithubRepos } from "../services/api";

const ANALYSIS_STEPS = 5;
const ANALYSIS_DURATION_MS = 5200;
const PROGRESS_TICK_MS = 50;

const GITHUB_URL_RE = /^https?:\/\/github\.com\/[^/\s]+\/[^/\s]+/i;

const MODES = [
  { id: "files", label: "Upload Files" },
  { id: "zip", label: "Upload ZIP" },
  { id: "github", label: "GitHub Repositories" },
];

export default function UploadPage({ onResults }) {
  const [mode, setMode] = useState("files");
  const [files, setFiles] = useState([]);
  const [repoUrl1, setRepoUrl1] = useState("");
  const [repoUrl2, setRepoUrl2] = useState("");
  const [loading, setLoading] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!loading) return undefined;

    const startedAt = Date.now();
    const interval = window.setInterval(() => {
      const elapsed = Date.now() - startedAt;
      const progress = Math.min((elapsed / ANALYSIS_DURATION_MS) * 100, 100);
      setAnalysisProgress(progress);
    }, PROGRESS_TICK_MS);

    return () => window.clearInterval(interval);
  }, [loading]);

  const isZipUpload = files.length === 1 && files[0].name.endsWith(".zip");

  async function runAnalysis(analysisPromise) {
    setError(null);
    setAnalysisProgress(0);
    setLoading(true);

    try {
      const minimumDelay = new Promise((resolve) =>
        window.setTimeout(resolve, ANALYSIS_DURATION_MS),
      );
      const [analysisResult] = await Promise.all([analysisPromise, minimumDelay]);
      onResults(analysisResult);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  function handleUploadSubmit(e) {
    e.preventDefault();

    if (!isZipUpload && files.length < 2) {
      setError("Please upload at least 2 files, or a single ZIP archive.");
      return;
    }

    runAnalysis(
      uploadFiles(files).then((uploadResult) => analyzeFiles(uploadResult.session_id)),
    );
  }

  function handleGithubSubmit(e) {
    e.preventDefault();

    const url1 = repoUrl1.trim();
    const url2 = repoUrl2.trim();

    if (!GITHUB_URL_RE.test(url1) || !GITHUB_URL_RE.test(url2)) {
      setError("Enter two valid GitHub repository URLs (https://github.com/user/repo).");
      return;
    }

    runAnalysis(compareGithubRepos(url1, url2));
  }

  function changeMode(nextMode) {
    setMode(nextMode);
    setError(null);
  }

  if (loading) {
    const currentStep = Math.min(
      Math.floor((analysisProgress / 100) * ANALYSIS_STEPS),
      ANALYSIS_STEPS - 1,
    );

    return <AnalysisLoader currentStep={currentStep} progress={analysisProgress} />;
  }

  return (
    <section className="page-card">
      <div className="hero-grid">
        <div className="page-header">
          <p className="eyebrow">AI-powered university MVP</p>
          <h1>Code Plagiarism Detector</h1>
          <p>
            Upload student submissions or compare two public GitHub repositories
            and identify suspicious similarity using CodeBERT embeddings, lexical
            overlap, and cosine scoring.
          </p>

          <div className="feature-chips" aria-label="Project features">
            <span>CodeBERT</span>
            <span>Hybrid scoring</span>
            <span>FastAPI</span>
            <span>React demo</span>
          </div>
        </div>

        <div className="hero-panel" aria-hidden="true">
          <div className="metric-card">
            <span>Similarity engine</span>
            <strong>Semantic + lexical</strong>
          </div>
          <div className="metric-card">
            <span>Risk labels</span>
            <strong>High / Medium / Low</strong>
          </div>
        </div>
      </div>

      <div className="mode-tabs" role="tablist" aria-label="Analysis mode">
        {MODES.map((item) => (
          <button
            key={item.id}
            type="button"
            role="tab"
            aria-selected={mode === item.id}
            className={`mode-tab ${mode === item.id ? "active" : ""}`}
            onClick={() => changeMode(item.id)}
          >
            {item.label}
          </button>
        ))}
      </div>

      {mode === "github" ? (
        <form className="upload-form" onSubmit={handleGithubSubmit}>
          <div className="github-form">
            <label className="field">
              <span className="field-label">Repository A URL</span>
              <input
                className="text-input"
                type="url"
                placeholder="https://github.com/user/project-a"
                value={repoUrl1}
                onChange={(e) => setRepoUrl1(e.target.value)}
                disabled={loading}
              />
            </label>
            <label className="field">
              <span className="field-label">Repository B URL</span>
              <input
                className="text-input"
                type="url"
                placeholder="https://github.com/user/project-b"
                value={repoUrl2}
                onChange={(e) => setRepoUrl2(e.target.value)}
                disabled={loading}
              />
            </label>
            <small className="field-hint">
              Public repositories only. Up to 100 source files per repo
              (.py, .java, .cs, .js). Large repositories are rejected.
            </small>
          </div>

          {error && <p className="error-message">{error}</p>}

          <button className="primary-button" type="submit" disabled={loading}>
            Analyze Repositories
          </button>
        </form>
      ) : (
        <form className="upload-form" onSubmit={handleUploadSubmit}>
          <label className="file-drop">
            <span className="file-icon" aria-hidden="true">
              &lt;/&gt;
            </span>
            <span className="file-drop-title">
              {mode === "zip" ? "Drop or select a ZIP archive" : "Drop or select code files"}
            </span>
            <small>
              {mode === "zip"
                ? "Upload a single ZIP archive containing source files (.py, .java, .cs, .js)"
                : "Upload multiple code files (.py, .java, .cs, .js)"}
            </small>
            <input
              className="file-input-hidden"
              type="file"
              multiple={mode !== "zip"}
              accept={mode === "zip" ? ".zip" : ".py,.java,.cs,.js"}
              onChange={(e) => setFiles(Array.from(e.target.files))}
              disabled={loading}
            />
          </label>

          {files.length > 0 && (
            <div className="selected-files">
              <strong>{files.length} file(s) selected</strong>
              <ul>
                {files.map((file) => (
                  <li key={`${file.name}-${file.size}`}>{file.name}</li>
                ))}
              </ul>
            </div>
          )}

          {error && <p className="error-message">{error}</p>}

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? "Analyzing submissions..." : "Analyze similarity"}
          </button>
        </form>
      )}
    </section>
  );
}
