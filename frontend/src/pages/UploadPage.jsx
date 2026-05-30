import { useEffect, useState } from "react";
import AnalysisLoader from "../components/AnalysisLoader";
import { uploadFiles, analyzeFiles } from "../services/api";

const ANALYSIS_STEPS = 5;
const ANALYSIS_DURATION_MS = 5200;
const PROGRESS_TICK_MS = 50;

export default function UploadPage({ onResults }) {
  const [files, setFiles] = useState([]);
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

  async function handleSubmit(e) {
    e.preventDefault();

    if (files.length < 2) {
      setError("Please upload at least 2 files to compare.");
      return;
    }

    setError(null);
    setAnalysisProgress(0);
    setLoading(true);

    try {
      const analysisPromise = uploadFiles(files).then((uploadResult) =>
        analyzeFiles(uploadResult.session_id),
      );
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

  if (loading) {
    const currentStep = Math.min(
      Math.floor((analysisProgress / 100) * ANALYSIS_STEPS),
      ANALYSIS_STEPS - 1,
    );

    return (
      <AnalysisLoader
        currentStep={currentStep}
        progress={analysisProgress}
      />
    );
  }

  return (
    <section className="page-card">
      <div className="hero-grid">
        <div className="page-header">
          <p className="eyebrow">AI-powered university MVP</p>
          <h1>Code Plagiarism Detector</h1>
          <p>
            Upload student submissions and identify suspicious similarity
            using CodeBERT embeddings, lexical overlap, and cosine scoring.
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

      <form className="upload-form" onSubmit={handleSubmit}>
        <label className="file-drop">
          <span className="file-icon" aria-hidden="true">
            &lt;/&gt;
          </span>
          <span className="file-drop-title">Drop or select code files</span>
          <small>Accepted formats: .py, .java, .cs, .js</small>
          <input
            className="file-input-hidden"
            type="file"
            multiple
            accept=".py,.java,.cs,.js"
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

      {loading && <AnalysisLoader />}
    </section>
  );
}
