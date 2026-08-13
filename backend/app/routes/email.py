from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.schemas.email import EmailRequest
from app.models.email_response import EmailResponse
from app.services.email_service import analyze_email
from app.services.report import report_service
from app.core.session import get_session_id

router = APIRouter(prefix="/email", tags=["Email Intelligence"])


@router.post("/analyze", response_model=EmailResponse)
def analyze(request: EmailRequest, session_id: str = Depends(get_session_id)):
    result = analyze_email(request.email)
    report_service.update_incident_source(session_id, "email", result)
    return result


@router.post("/upload")
async def upload_email(file: UploadFile = File(...), session_id: str = Depends(get_session_id)):
    if not file.filename.lower().endswith(".eml"):
        raise HTTPException(status_code=400, detail="Please upload a .eml file.")

    raw_email = (await file.read()).decode("utf-8", errors="ignore")

    result = analyze_email(raw_email)
    try:
        report_service.update_incident_source(session_id, "email", result)
    except Exception:
        pass
    return result