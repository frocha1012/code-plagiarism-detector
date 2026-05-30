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
