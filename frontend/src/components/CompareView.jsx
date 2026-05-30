/**
 * Side-by-side file content comparison.
 * Day 4 task: render two code blocks with highlighted differences.
 */
export default function CompareView({ fileA, fileB, contentA, contentB }) {
  return (
    <div style={{ display: "flex", gap: "1rem" }}>
      <div style={{ flex: 1 }}>
        <h3>{fileA}</h3>
        <pre>{contentA}</pre>
      </div>
      <div style={{ flex: 1 }}>
        <h3>{fileB}</h3>
        <pre>{contentB}</pre>
      </div>
    </div>
  );
}
