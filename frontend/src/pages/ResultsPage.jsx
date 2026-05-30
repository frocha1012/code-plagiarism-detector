import { useState } from "react";
import CompareView from "../components/CompareView";
import SimilarityTable from "../components/SimilarityTable";
import { getSimilarSections } from "../services/api";

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

        <button className="secondary-button" onClick={onReset}>
          Upload New Files
        </button>
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
