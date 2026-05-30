const BASE_URL = "http://localhost:8000/api";

/**
 * Uploads multiple files to the backend.
 * Returns { session_id, uploaded, count }.
 */
export async function uploadFiles(files) {
  const form = new FormData();
  files.forEach((file) => form.append("files", file));

  const res = await fetch(`${BASE_URL}/upload`, { method: "POST", body: form });
  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

/**
 * Triggers similarity analysis for a session.
 * Returns { session_id, pairs[] }.
 */
export async function analyzeFiles(sessionId) {
  const res = await fetch(`${BASE_URL}/analyze?session_id=${sessionId}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Analysis failed");
  return res.json();
}

/**
 * Fetches stored results for a session.
 */
export async function getResults(sessionId) {
  const res = await fetch(`${BASE_URL}/results/${sessionId}`);
  if (!res.ok) throw new Error("Failed to fetch results");
  return res.json();
}
