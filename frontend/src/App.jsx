import { useState } from "react";
import UploadPage from "./pages/UploadPage";
import ResultsPage from "./pages/ResultsPage";

export default function App() {
  const [analysisResult, setAnalysisResult] = useState(null);

  return (
    <main className="app-shell">
      {!analysisResult ? (
        <UploadPage onResults={setAnalysisResult} />
      ) : (
        <ResultsPage
          results={analysisResult}
          onReset={() => setAnalysisResult(null)}
        />
      )}
    </main>
  );
}
