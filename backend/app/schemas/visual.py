from pydantic import BaseModel
from typing import List, Optional


class VisualRequest(BaseModel):
    image_path: Optional[str] = None


class SimilarityMetrics(BaseModel):
    visual: float
    logo: float
    color: float
    layout: float


class OCRResult(BaseModel):
    text: List[str]


class QRResult(BaseModel):
    detected: bool
    data: Optional[str] = None


class LogoResult(BaseModel):
    detected: bool
    brand: Optional[str] = None
    confidence: float


class VisualResponse(BaseModel):
    overallRisk: int
    verdict: str

    detectedBrand: Optional[str]

    similarity: SimilarityMetrics

    ocr: OCRResult

    qr: QRResult

    logo: LogoResult

    explanation: str

    recommendations: List[str]