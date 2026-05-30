import { useState } from "react";
import UploadPage from "./pages/UploadPage";
import ResultsPage from "./pages/ResultsPage";

export default function App() {
  const [results, setResults] = useState(null);

  return (
    <div>
      {!results ? (
        <UploadPage onResults={setResults} />
      ) : (
        <ResultsPage results={results} onReset={() => setResults(null)} />
      )}
    </div>
  );
}
