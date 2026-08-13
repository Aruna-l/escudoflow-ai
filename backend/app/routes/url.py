from fastapi import APIRouter, Depends

from app.models.request_models import URLRequest
from app.models.response_models import URLResponse
from app.services.url_service import analyze_url
from app.services.report import report_service
from app.core.session import get_session_id

router = APIRouter(prefix="/url", tags=["URL Intelligence"])


@router.post("/analyze", response_model=URLResponse)
def analyze(request: URLRequest, session_id: str = Depends(get_session_id)):
    result = analyze_url(request.url)

    report_payload = {**report_service._as_dict(result), "analyzed_url": request.url}
    try:
        report_service.update_incident_source(session_id, "url", report_payload)
    except Exception:
        pass
    return result