from fastapi import Header


def get_session_id(x_session_id: str = Header(default="anonymous-session", alias="X-Session-Id")) -> str:
    """
    Every request from the frontend carries a per-browser-tab session id
    (see frontend/src/lib/session-id.ts). Requests without the header
    (e.g. manual Postman testing) fall back to a shared 'anonymous-session'
    bucket so nothing breaks, but concurrent real users each get their own
    isolated rolling incident.
    """
    return x_session_id