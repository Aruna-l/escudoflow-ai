from pydantic import BaseModel
from typing import List, Dict


class VisualResponse(BaseModel):

    brand: str

    verdict: str

    riskScore: int

    similarity: Dict

    screenshot: str

    referenceImage: str

    explanation: str

    indicators: List[str]