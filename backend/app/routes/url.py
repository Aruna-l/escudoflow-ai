from fastapi import APIRouter

from app.models.request_models import URLRequest
from app.models.response_models import URLResponse
from app.services.url_service import analyze_url

router = APIRouter(
    prefix="/url",
    tags=["URL Intelligence"]
)


@router.post("/analyze", response_model=URLResponse)
def analyze(request: URLRequest):
    return analyze_url(request.url)