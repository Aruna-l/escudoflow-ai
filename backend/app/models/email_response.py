from typing import List, Dict, Any
from pydantic import BaseModel


class EmailResponse(BaseModel):

    # Email Information
    from_email: str
    reply_to: str
    subject: str
    body: str

    # Overall Verdict
    overallRisk: int
    confidence: int
    verdict: str

    # Dashboard Metrics
    phishingProbability: float
    bec: bool
    spamScore: float
    urgency: float
    impersonation: float
    reputation: str

    # Authentication
    authentication: Dict[str, Any]
    headerSummary: str

    # Reply-To
    reply_analysis: Dict[str, Any]
    senderReputation: str

    # Entity Recognition
    entities: Dict[str, Any]

    # URLs
    urls: List[Dict[str, Any]]

    # Attachments
    attachments: List[Dict[str, Any]]

    # Rule Engine
    rule_engine: Dict[str, Any]

    # Highlighted Sentences
    highlighted: List[Dict[str, Any]]

    # AI Explanation
    aiExplanation: Dict[str, Any]