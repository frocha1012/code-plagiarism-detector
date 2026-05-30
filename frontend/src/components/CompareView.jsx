const KEYWORDS = new Set([
  "and", "as", "assert", "async", "await", "break", "class", "continue",
  "def", "del", "elif", "else", "except", "false", "finally", "for", "from",
  "global", "if", "import", "in", "is", "lambda", "none", "nonlocal", "not",
  "or", "pass", "raise", "return", "true", "try", "while", "with", "yield",
  "self", "print",
]);

// Lightweight Python-ish syntax highlighter (no external libraries).
// Splits a line into typed tokens and wraps them in styled spans.
function highlightLine(line) {
  const tokenRegex =
    /(\s+)|(#.*)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|([^\sA-Za-z0-9_]+)/g;

  const nodes = [];
  let match;
  let key = 0;

  while ((match = tokenRegex.exec(line)) !== null) {
    const [, space, comment, string, number, word, symbol] = match;

    if (space) {
      nodes.push(space);
    } else if (comment) {
      nodes.push(<span key={key++} className="tok-comment">{comment}</span>);
    } else if (string) {
      nodes.push(<span key={key++} className="tok-string">{string}</span>);
    } else if (number) {
      nodes.push(<span key={key++} className="tok-number">{number}</span>);
    } else if (word) {
      const lower = word.toLowerCase();
      if (KEYWORDS.has(lower)) {
        nodes.push(<span key={key++} className="tok-keyword">{word}</span>);
      } else {
        // identifier directly followed by "(" is treated as a function name
        const next = line.slice(tokenRegex.lastIndex).trimStart()[0];
        const cls = next === "(" ? "tok-function" : "tok-identifier";
        nodes.push(<span key={key++} className={cls}>{word}</span>);
      }
    } else if (symbol) {
      nodes.push(<span key={key++} className="tok-symbol">{symbol}</span>);
    }
  }

  return nodes;
}

// Groups matches whose line numbers are consecutive on BOTH sides, so a
// straight run of similar lines (e.g. a function body) shows as one box
// instead of many single-line boxes.
function groupMatches(matches) {
  const sorted = [...matches].sort((a, b) => a.file1_line - b.file1_line);
  const groups = [];

  for (const match of sorted) {
    const current = groups[groups.length - 1];
    const last = current && current[current.length - 1];

    if (
      last &&
      match.file1_line === last.file1_line + 1 &&
      match.file2_line === last.file2_line + 1
    ) {
      current.push(match);
    } else {
      groups.push([match]);
    }
  }

  return groups;
}

export default function CompareView({ comparison, onBack }) {
  const matches = comparison.matches || [];
  const groups = groupMatches(matches);
  const pairScore =
    typeof comparison.pairScore === "number"
      ? comparison.pairScore
      : matches.length
        ? Math.max(...matches.map((match) => match.similarity))
        : 0;

  return (
    <section className="page-card compare-view">
      <button className="back-link" onClick={onBack}>
        <span aria-hidden="true">←</span> Back to Results
      </button>

      <div className="compare-top">
        <div className="compare-title">
          <span className="compare-icon" aria-hidden="true">&lt;/&gt;</span>
          <div>
            <h1>Similar Code Lines</h1>
            <p>Showing lines that are most likely similar in both files.</p>
          </div>
        </div>

        <div className="match-stat-card">
          <span className="stat-spark" aria-hidden="true">✦</span>
          <div>
            <strong>{matches.length}</strong>
            <span>Matching Lines Found</span>
          </div>
        </div>
      </div>

      {matches.length > 0 ? (
        <div className="code-compare-panel">
          <div className="code-compare-head">
            <span className="file-tag">
              <span aria-hidden="true">📄</span> {comparison.file1}
            </span>
            <span className="similar-pill">✓ Similar</span>
            <span className="file-tag right">
              <span aria-hidden="true">📄</span> {comparison.file2}
            </span>
          </div>

          <div className="code-compare-body">
            {groups.map((group, groupIndex) => (
              <div
                className="code-row"
                key={`${group[0].file1_line}-${group[0].file2_line}-${groupIndex}`}
              >
                <div className="code-block">
                  {group.map((match, i) => (
                    <div className="code-line" key={`l-${match.file1_line}-${i}`}>
                      <span className="ln">{match.file1_line}</span>
                      <code>{highlightLine(match.file1_text)}</code>
                    </div>
                  ))}
                </div>

                <span className="row-arrow" aria-hidden="true">↔</span>

                <div className="code-block">
                  {group.map((match, i) => (
                    <div className="code-line" key={`r-${match.file2_line}-${i}`}>
                      <span className="ln">{match.file2_line}</span>
                      <code>{highlightLine(match.file2_text)}</code>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="code-compare-foot">
            <span className="foot-note">
              <span className="foot-icon" aria-hidden="true">ℹ</span>
              Only highly similar lines are shown to help you focus on the
              important matches.
            </span>
            <span className="foot-score">
              Similarity Score: <strong>{(pairScore * 100).toFixed(1)}%</strong>
            </span>
          </div>
        </div>
      ) : (
        <div className="empty-state">
          <h2>No direct line matches found</h2>
          <p>
            The pair may be semantically related, but no line-level matches
            exceeded the threshold.
          </p>
        </div>
      )}
    </section>
  );
}
