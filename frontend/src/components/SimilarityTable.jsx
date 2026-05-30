const explanations = {
  high: "High semantic similarity and lexical overlap detected. Potential variable renaming pattern.",
  medium: "Some structural similarities detected. Manual review recommended.",
  low: "Limited similarity detected. Likely unrelated implementations.",
};

export default function SimilarityTable({ pairs = [], onCompare, loadingPair }) {
  if (pairs.length === 0) {
    return <p className="empty-state">No similarity results found.</p>;
  }

  return (
    <div className="results-list">
      {pairs.map((pair, i) => {
        const canCompare = pair.level === "high" || pair.level === "medium";
        const pairKey = `${pair.file1}-${pair.file2}`;

        return (
          <article
            className={`result-card ${pair.level}`}
            key={`${pair.file1}-${pair.file2}-${i}`}
          >
            <div>
              <p className="result-label">Compared files</p>
              <div className="file-pair">
                <span>{pair.file1}</span>
                <span className="pair-divider">vs</span>
                <span>{pair.file2}</span>
              </div>
              <p className="result-explanation">
                {explanations[pair.level] || explanations.low}
              </p>
            </div>

            <div className="score-block">
              <span className="score-value">{(pair.score * 100).toFixed(1)}%</span>

              {canCompare ? (
                <>
                  <span className={`risk-badge ${pair.level}`}>{pair.level}</span>
                  <button
                    className="compare-button"
                    type="button"
                    onClick={() => onCompare?.(pair)}
                    disabled={loadingPair === pairKey}
                  >
                    {loadingPair === pairKey ? "Loading..." : "Compare Files"}
                  </button>
                </>
              ) : (
                <div className="low-risk-note">
                  <span className="risk-badge low">low risk</span>
                  <span>No significant similarities detected</span>
                </div>
              )}
            </div>
          </article>
        );
      })}
    </div>
  );
}
