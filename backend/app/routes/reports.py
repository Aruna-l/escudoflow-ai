from fastapi import APIRouter, HTTPException, Response, Depends
from app.schemas.report import ReportGenerateRequest, ReportResponse, ReportListItem, ReportNotesUpdate
from app.services.report import report_service
from app.core.session import get_session_id
from app.schemas.report import (
    ReportGenerateRequest, ReportResponse, ReportListItem,
    ReportNotesUpdate, ReportStatusUpdate,
)


router = APIRouter(prefix="/report", tags=["Reports"])


@router.post("/generate", response_model=ReportResponse)
async def generate(payload: ReportGenerateRequest):
    try:
        return report_service.generate_report(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/latest", response_model=ReportResponse)
async def latest(session_id: str = Depends(get_session_id)):
    report = report_service.get_latest_report(session_id)
    if not report:
        raise HTTPException(status_code=404, detail="No live report for this session yet")
    return report


@router.post("/reset")
async def reset(session_id: str = Depends(get_session_id)):
    report_service.reset_incident(session_id)
    return {"status": "ok"}


@router.get("/", response_model=list[ReportListItem])
async def list_all():
    return report_service.list_reports()


@router.get("/{report_id}", response_model=ReportResponse)
async def get_one(report_id: str):
    report = report_service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.patch("/{report_id}/notes", response_model=ReportResponse)
async def update_notes(report_id: str, payload: ReportNotesUpdate):
    report = report_service.update_notes(report_id, payload.notes)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/{report_id}/export/json")
async def export_json(report_id: str):
    import json
    report = report_service.export_json(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return Response(
        content=json.dumps(report, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{report_id}.json"'},
    )


@router.get("/{report_id}/export/csv")
async def export_csv(report_id: str):
    csv_data = report_service.export_csv(report_id)
    if csv_data is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{report_id}.csv"'},
    )


@router.get("/{report_id}/export/pdf")
async def export_pdf(report_id: str):
    pdf_bytes = report_service.export_pdf(report_id)
    if pdf_bytes is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{report_id}.pdf"'},
    )

@router.patch("/{report_id}/status", response_model=ReportResponse)
async def update_status(report_id: str, payload: ReportStatusUpdate):
    try:
        report = report_service.update_status(report_id, payload.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report