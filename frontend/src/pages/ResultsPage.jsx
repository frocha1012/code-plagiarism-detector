import { useState } from "react";
import CompareView from "../components/CompareView";
import SimilarityTable from "../components/SimilarityTable";
import { explainPair, exportPdfReport, getSimilarSections } from "../services/api";

const techStack = [
  "CodeBERT",
  "FastAPI",
  "React",
  "Hybrid Similarity Scoring",
  "Cosine Similarity",
];

export default function ResultsPage({ results, onReset }) {
  const pairs = results.pairs || [];
  const uniqueFiles = new Set(pairs.flatMap((pair) => [pair.file1, pair.file2]));
  const suspiciousPairs = pairs.filter((pair) => pair.level === "high").length;
  const highestScore = pairs.length
    ? Math.max(...pairs.map((pair) => pair.score))
    : 0;
  const [comparison, setComparison] = useState(null);
  const [compareError, setCompareError] = useState(null);
  const [loadingPair, setLoadingPair] = useState(null);
  const [explanations, setExplanations] = useState({});   // pairKey -> text
  const [loadingExplain, setLoadingExplain] = useState(null); // pairKey | null
  const [exportingReport, setExportingReport] = useState(false);
  const [reportError, setReportError] = useState(null);

  async function handleCompare(pair) {
    const pairKey = `${pair.file1}-${pair.file2}`;
    setLoadingPair(pairKey);
    setCompareError(null);

    try {
      const comparisonResult = await getSimilarSections(
        results.session_id,
        pair.file1,
        pair.file2,
      );

      setComparison({ ...comparisonResult, pairScore: pair.score, level: pair.level });
    } catch (err) {
      setCompareError(err.message || "Could not load files for comparison.");
    } finally {
      setLoadingPair(null);
    }
  }

  async function handleExplain(pair) {
    const pairKey = `${pair.file1}-${pair.file2}`;
    if (explanations[pairKey]) return; // already fetched
    setLoadingExplain(pairKey);

    try {
      const data = await explainPair(
        results.session_id,
        pair.file1,
        pair.file2,
        pair.score,
        pair.level,
      );
      setExplanations((prev) => ({ ...prev, [pairKey]: data.explanation }));
    } catch {
      setExplanations((prev) => ({
        ...prev,
        [pairKey]: "AI explanation unavailable. Please review manually.",
      }));
    } finally {
      setLoadingExplain(null);
    }
  }

  async function handleExportReport() {
    setExportingReport(true);
    setReportError(null);

    try {
      const reportBlob = await exportPdfReport(results.session_id);
      const downloadUrl = URL.createObjectURL(reportBlob);
      const link = document.createElement("a");

      link.href = downloadUrl;
      link.download = `plagiarism-report-${results.session_id}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(downloadUrl);
    } catch (err) {
      setReportError(err.message || "Could not export PDF report.");
    } finally {
      setExportingReport(false);
    }
  }

  if (comparison) {
    return (
      <CompareView
        comparison={comparison}
        onBack={() => setComparison(null)}
      />
    );
  }

  return (
    <section className="page-card">
      <div className="results-header">
        <div className="page-header">
          <p className="eyebrow">Analysis complete</p>
          <h1>Similarity Results</h1>
        </div>

        <div className="result-actions">
          <button
            className="secondary-button"
            onClick={handleExportReport}
            disabled={exportingReport}
          >
            {exportingReport ? "Exporting..." : "Export PDF Report"}
          </button>
          <button className="secondary-button" onClick={onReset}>
            Upload New Files
          </button>
        </div>
      </div>

      <div className="summary-grid">
        <div className="summary-card">
          <span>Files analyzed</span>
          <strong>{uniqueFiles.size}</strong>
        </div>
        <div className="summary-card">
          <span>Suspicious pairs</span>
          <strong>{suspiciousPairs}</strong>
        </div>
        <div className="summary-card">
          <span>Highest score</span>
          <strong>{(highestScore * 100).toFixed(1)}%</strong>
        </div>
      </div>

      {pairs.length > 0 ? (
        <SimilarityTable
          pairs={pairs}
          onCompare={handleCompare}
          loadingPair={loadingPair}
          onExplain={handleExplain}
          loadingExplain={loadingExplain}
          explanations={explanations}
        />
      ) : (
        <div className="empty-state">
          <h2>No analysis results available</h2>
          <p>Upload at least two supported code files to run a new comparison.</p>
          <button className="primary-button" onClick={onReset}>
            Analyze New Files
          </button>
        </div>
      )}

      {compareError && <p className="error-message">{compareError}</p>}
      {reportError && <p className="error-message">{reportError}</p>}

      <section className="tech-stack">
        <p className="eyebrow">Technology Stack</p>
        <div className="tech-chips">
          {techStack.map((item) => (
            <span key={item}>{item}</span>
          ))}
        </div>
      </section>

      <p className="session-footer">
        Session ID: <code>{results.session_id}</code>
      </p>
    </section>
  );
}
