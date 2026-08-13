from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.core.constants import SUPPORTED_UPLOAD_EXTENSIONS, MAX_UPLOAD_SIZE_MB
from app.schemas.attachment import AttachmentAnalysisResponse
from app.services.attachment.attachment_service import analyze_attachment_file
from app.services.report import report_service
from app.core.session import get_session_id

router = APIRouter(prefix="/attachment", tags=["Attachment Intelligence"])


@router.post("/analyze", response_model=AttachmentAnalysisResponse)
async def analyze_attachment(
    file: UploadFile = File(...),
    session_id: str = Depends(get_session_id)
):
    filename = file.filename or ""
    extension = (
        ("." + filename.rsplit(".", 1)[-1].lower())
        if "." in filename
        else ""
    )

    if extension not in SUPPORTED_UPLOAD_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{extension or 'unknown'}'. "
                "Supported: PDF, DOCX, ZIP, RAR, EXE, JS and related office/script formats."
            ),
        )

    data = await file.read()

    if len(data) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024

    if len(data) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds the {MAX_UPLOAD_SIZE_MB}MB limit."
        )

    try:
        result = analyze_attachment_file(
            filename=filename,
            data=data
        )

        # Keep report updating independent from file analysis.
        # If report updating fails, the analysis result is still returned.
        try:
            report_service.update_incident_source(
                session_id,
                "attachment",
                result
            )
        except Exception:
            pass

        return result

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze attachment: {exc}"
        )