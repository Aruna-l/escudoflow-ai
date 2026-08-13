from fastapi import APIRouter, HTTPException, Depends
from app.schemas.threat import ThreatAnalyzeRequest, ThreatIntelResponse
from app.services.threat.threat_service import analyze_ioc
from app.services.report import report_service
from app.core.session import get_session_id

router = APIRouter(prefix="/threat", tags=["Threat Intelligence"])


@router.post("/analyze", response_model=ThreatIntelResponse)
async def analyze_threat(payload: ThreatAnalyzeRequest, session_id: str = Depends(get_session_id)):
    try:
        result = await analyze_ioc(payload.ioc.strip(), payload.type)
        report_service.update_incident_source(session_id, "threat", result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))