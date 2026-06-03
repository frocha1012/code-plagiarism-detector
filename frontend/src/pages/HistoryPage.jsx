import { useEffect, useState } from "react";
import {
  getHistory,
  getHistorySession,
  deleteHistorySession,
} from "../services/api";

function formatDate(isoString) {
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return "Unknown date";
  return date.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function HistoryPage({ onOpen }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openingId, setOpeningId] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(null); // session_id | null
  const [deletingId, setDeletingId] = useState(null);

  async function loadHistory() {
    setLoading(true);
    setError(null);
    try {
      setItems(await getHistory());
    } catch (err) {
      setError(err.message || "Could not load history.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  async function handleView(sessionId) {
    setOpeningId(sessionId);
    setError(null);
    try {
      const analysis = await getHistorySession(sessionId);
      onOpen(analysis);
    } catch (err) {
      setError(err.message || "Could not open this analysis.");
      setOpeningId(null);
    }
  }

  async function handleDelete(sessionId) {
    setDeletingId(sessionId);
    try {
      await deleteHistorySession(sessionId);
      setItems((prev) => prev.filter((item) => item.session_id !== sessionId));
    } catch (err) {
      setError(err.message || "Could not delete this session.");
    } finally {
      setDeletingId(null);
      setConfirmDelete(null);
    }
  }

  return (
    <section className="page-card">
      <div className="page-header">
        <p className="eyebrow">Saved analyses</p>
        <h1>Analysis History</h1>
        <p>Revisit a previous comparison or remove it from storage.</p>
      </div>

      {error && <p className="error-message">{error}</p>}

      {loading ? (
        <p className="history-status">Loading history…</p>
      ) : items.length === 0 ? (
        <div className="empty-state">
          <h2>No analyses yet</h2>
          <p>Run a comparison from the home page and it will appear here.</p>
        </div>
      ) : (
        <div className="history-list">
          {items.map((item) => (
            <article className="history-card" key={item.session_id}>
              <div className="history-main">
                <span className="history-date">{formatDate(item.created_at)}</span>
                <div className="history-meta">
                  <span>
                    <strong>{item.file_count}</strong> file
                    {item.file_count === 1 ? "" : "s"}
                  </span>
                  <span>
                    Highest score{" "}
                    <strong>{(item.highest_score * 100).toFixed(1)}%</strong>
                  </span>
                  {item.high_risk_pairs > 0 ? (
                    <span className="risk-badge high">
                      {item.high_risk_pairs} high-risk pair
                      {item.high_risk_pairs === 1 ? "" : "s"}
                    </span>
                  ) : (
                    <span className="risk-badge low">No high-risk pairs</span>
                  )}
                </div>
                <code className="history-session-id">{item.session_id}</code>
              </div>

              <div className="history-actions">
                <button
                  className="compare-button"
                  type="button"
                  onClick={() => handleView(item.session_id)}
                  disabled={openingId === item.session_id}
                >
                  {openingId === item.session_id ? "Opening…" : "View Results"}
                </button>
                <button
                  className="delete-button"
                  type="button"
                  onClick={() => setConfirmDelete(item.session_id)}
                  disabled={deletingId === item.session_id}
                >
                  Delete
                </button>
              </div>
            </article>
          ))}
        </div>
      )}

      {confirmDelete && (
        <div
          className="modal-overlay"
          role="dialog"
          aria-modal="true"
          onClick={() => setConfirmDelete(null)}
        >
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <h2>Delete this analysis?</h2>
            <p>
              This permanently removes the session and all of its uploaded
              files. This action cannot be undone.
            </p>
            <div className="modal-actions">
              <button
                className="secondary-button"
                type="button"
                onClick={() => setConfirmDelete(null)}
                disabled={deletingId === confirmDelete}
              >
                Cancel
              </button>
              <button
                className="delete-button"
                type="button"
                onClick={() => handleDelete(confirmDelete)}
                disabled={deletingId === confirmDelete}
              >
                {deletingId === confirmDelete ? "Deleting…" : "Delete Session"}
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
