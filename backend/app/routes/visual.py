from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, Form, Depends

from app.services.visual.visual_service import analyze_visual
from app.services.report import report_service
from app.core.session import get_session_id

router = APIRouter(prefix="/visual", tags=["Visual Intelligence"])

UPLOAD_DIR = Path("uploads/visual")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/analyze")
async def analyze_visual_image(
    file: UploadFile = File(...),
    url: str = Form(default=""),
    session_id: str = Depends(get_session_id),
):
    extension = Path(file.filename).suffix
    save_path = UPLOAD_DIR / f"uploaded{extension}"

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_visual(str(save_path), user_url=url)

    report_payload = {**report_service._as_dict(result), "targetUrl": url}
    try:
        report_service.update_incident_source(session_id, "visual", report_payload, target=url or None)
    except Exception:
        pass
    return result