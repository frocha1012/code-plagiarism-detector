const BASE_URL = "http://localhost:8000/api";

export async function uploadFiles(files) {
  const form = new FormData();
  files.forEach((file) => form.append("files", file));

  const res = await fetch(`${BASE_URL}/upload`, { method: "POST", body: form });
  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Upload failed");
  }

  return res.json();
}

export async function analyzeFiles(sessionId) {
  const res = await fetch(`${BASE_URL}/analyze?session_id=${sessionId}`, {
    method: "POST",
  });

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Analysis failed");
  }

  return res.json();
}

export async function getFileContent(sessionId, filename) {
  const encodedSessionId = encodeURIComponent(sessionId);
  const encodedFilename = encodeURIComponent(filename);
  const res = await fetch(`${BASE_URL}/files/${encodedSessionId}/${encodedFilename}`);

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Failed to load file content");
  }

  return res.json();
}

export async function getSimilarSections(sessionId, file1, file2) {
  const params = new URLSearchParams({
    file1,
    file2,
  });
  const encodedSessionId = encodeURIComponent(sessionId);
  const res = await fetch(`${BASE_URL}/compare/${encodedSessionId}?${params}`);

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Failed to compare files");
  }

  return res.json();
}

export async function generateSummary(sessionId, pairs) {
  const res = await fetch(`${BASE_URL}/summary`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, pairs }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Failed to generate summary");
  }

  return res.json(); // { summary: "..." }
}

export async function explainPair(sessionId, file1, file2, score, level) {
  const res = await fetch(`${BASE_URL}/explain`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, file1, file2, score, level }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Failed to get AI explanation");
  }

  return res.json(); // { explanation: "..." }
}

export async function compareGithubRepos(repoUrl1, repoUrl2) {
  const res = await fetch(`${BASE_URL}/github/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repo_url_1: repoUrl1, repo_url_2: repoUrl2 }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Repository comparison failed");
  }

  return res.json(); // { session_id, pairs }
}

export async function getHistory() {
  const res = await fetch(`${BASE_URL}/history`);

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Failed to load history");
  }

  return res.json(); // [{ session_id, created_at, file_count, highest_score, high_risk_pairs }]
}

export async function getHistorySession(sessionId) {
  const encodedSessionId = encodeURIComponent(sessionId);
  const res = await fetch(`${BASE_URL}/history/${encodedSessionId}`);

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Failed to load saved analysis");
  }

  return res.json(); // { session_id, pairs }
}

export async function deleteHistorySession(sessionId) {
  const encodedSessionId = encodeURIComponent(sessionId);
  const res = await fetch(`${BASE_URL}/history/${encodedSessionId}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Failed to delete session");
  }

  return res.json();
}

export async function getMeta() {
  const res = await fetch(`${BASE_URL}/meta`);

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Failed to load project info");
  }

  return res.json(); // { thresholds: { high, medium }, statistics: {...} }
}

export async function exportPdfReport(sessionId) {
  const encodedSessionId = encodeURIComponent(sessionId);
  const res = await fetch(`${BASE_URL}/report/${encodedSessionId}`);

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "Failed to export PDF report");
  }

  return res.blob();
}
