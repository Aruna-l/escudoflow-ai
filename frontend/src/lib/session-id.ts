const SESSION_KEY = "escudoflow_session_id";

/** One stable ID per browser (persisted in localStorage), sent as the
 * X-Session-Id header on every analyze/report call so the backend keeps
 * each tab/user's rolling incident isolated from everyone else's. */
export function getSessionId(): string {
  let id = localStorage.getItem(SESSION_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, id);
  }
  return id;
}