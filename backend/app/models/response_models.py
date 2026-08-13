from typing import List, Dict, Any
from pydantic import BaseModel


class URLResponse(BaseModel):

    # -----------------------------
    # Basic URL Information
    # -----------------------------
    url: str
    domain: str
    protocol: str
    url_length: int
    https: bool

    # -----------------------------
    # Final Prediction
    # -----------------------------
    prediction: str
    confidence: float
    risk_score: float
    severity: str

    # -----------------------------
    # ML + Rule Engine
    # -----------------------------
    ml_prediction: str
    ml_risk_score: float
    rule_score: int
    reasons: List[str]

    # -----------------------------
    # Threat Intelligence
    # -----------------------------
    reputation: Dict[str, Any]

    # -----------------------------
    # Domain Intelligence
    # -----------------------------
    whois: Dict[str, Any]
    dns: Dict[str, Any]
    ssl: Dict[str, Any]
    hosting: Dict[str, Any]

    # -----------------------------
    # Brand Analysis
    # -----------------------------
    brand_similarity: Dict[str, Any]

    # -----------------------------
    # Redirect chain
    # -----------------------------
    redirects: list[str] = []
    redirect_count: int = 0
    final_url: str = ""

    # -----------------------------
    # Behaviour Timeline
    # -----------------------------
    timeline: list = []

    ai_explanation: dict = {}