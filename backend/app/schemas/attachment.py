from typing import List

from pydantic import BaseModel, Field

# NOTE: field names below are camelCase and FLAT on purpose — they match
# the shape of ATTACHMENT_ANALYSIS_MOCK in the frontend's lib/mock-data
# exactly, so the frontend can swap the mock object for the fetched
# response with zero reshaping.


class ThreatItem(BaseModel):
    name: str
    severity: str  # safe | low | suspicious | high | critical — matches RiskBadge's `level` prop


class AttachmentAnalysisResponse(BaseModel):
    riskScore: int = Field(..., ge=0, le=100)
    riskLabel: str  # safe | low | suspicious | high | critical (extra field, safe for frontend to ignore)
    fileName: str
    fileType: str
    size: str  # formatted, e.g. "184 KB"
    macros: bool
    embeddedScripts: int
    suspiciousExecutables: int
    sha256: str
    threats: List[ThreatItem]
    recommendation: str
