import SimilarityTable from "../components/SimilarityTable";

export default function ResultsPage({ results, onReset }) {
  return (
    <div>
      <h1>Analysis Results</h1>
      <button onClick={onReset}>Upload New Files</button>
      <SimilarityTable pairs={results.pairs} />
    </div>
  );
}
