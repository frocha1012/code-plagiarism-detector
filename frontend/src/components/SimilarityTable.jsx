/**
 * Renders the similarity results as a sortable table.
 * Day 4 task: implement row click to open CompareView.
 */
export default function SimilarityTable({ pairs = [] }) {
  if (pairs.length === 0) {
    return <p>No results yet.</p>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>File A</th>
          <th>File B</th>
          <th>Score</th>
          <th>Level</th>
        </tr>
      </thead>
      <tbody>
        {pairs.map((pair, i) => (
          <tr key={i}>
            <td>{pair.file_a}</td>
            <td>{pair.file_b}</td>
            <td>{(pair.score * 100).toFixed(1)}%</td>
            <td>{pair.level}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
