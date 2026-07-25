from typing import List
from pydantic import BaseModel


class URLResponse(BaseModel):
    url: str
    domain: str
    protocol: str
    url_length: int
    https: bool

    prediction: str
    confidence: float
    risk_score: int
    reasons: List[str]