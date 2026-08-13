from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

Severity = Literal["Critical", "High", "Suspicious", "Low", "Safe"]
ReportStatus = Literal["Investigating", "Blocked", "Escalated", "Resolved"]


class IOCItem(BaseModel):
    type: str
    value: str


class TimelineEvent(BaseModel):
    t: str
    event: str


class ThreatOverview(BaseModel):
    vector: str
    target: str
    impact: str


class EvidenceItem(BaseModel):
    filename: str
    sourceType: str  # "email" | "url" | "attachment" | "visual" | "threat"


class ReportGenerateRequest(BaseModel):
    """
    Pass the raw JSON responses you already get back from
    /email/analyze, /url/analyze, /attachment/analyze, /threat/analyze,
    /visual/analyze. Any subset can be omitted.
    """
    title: Optional[str] = None
    analyst: Optional[str] = "EscudoFlow AI"
    target: Optional[str] = Field(
        None, description="e.g. 'CFO / Finance' — who/what was targeted"
    )
    notes: Optional[str] = None

    email: Optional[Dict[str, Any]] = None
    url: Optional[Dict[str, Any]] = None
    threat: Optional[Dict[str, Any]] = None
    attachment: Optional[Dict[str, Any]] = None
    visual: Optional[Dict[str, Any]] = None


class ReportNotesUpdate(BaseModel):
    notes: str


class ReportStatusUpdate(BaseModel):
    status: ReportStatus


class ReportListItem(BaseModel):
    id: str
    title: str
    createdAt: str
    analyst: str
    severity: Severity
    riskScore: int
    status: ReportStatus


class ReportResponse(BaseModel):
    id: str
    title: str
    createdAt: str
    analyst: str
    severity: Severity
    riskScore: int
    confidence: int
    executiveSummary: str
    threatOverview: ThreatOverview
    iocs: List[IOCItem]
    timeline: List[TimelineEvent]
    recommendations: List[str]
    evidence: List[EvidenceItem]
    analystNotes: Optional[str] = None
    sourceCountry: str = "Unknown"
    status: ReportStatus = "Investigating"