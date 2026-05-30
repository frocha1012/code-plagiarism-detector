import { useState } from "react";
import { uploadFiles, analyzeFiles } from "../services/api";

export default function UploadPage({ onResults }) {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (files.length < 2) {
      setError("Please upload at least 2 files to compare.");
      return;
    }
    // TODO Day 1: call uploadFiles(), then analyzeFiles(), then onResults(data)
    setLoading(true);
    setError(null);
  }

  return (
    <div>
      <h1>Code Plagiarism Detector</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          multiple
          accept=".py,.java,.cs,.js,.ts,.cpp,.c"
          onChange={(e) => setFiles(Array.from(e.target.files))}
        />
        {files.length > 0 && <p>{files.length} file(s) selected</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>
    </div>
  );
}
