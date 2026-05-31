from io import BytesIO

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.services.report_service import generate_pdf_report

router = APIRouter(tags=["report"])


@router.get("/report/{session_id}")
def export_report(session_id: str):
    """Returns a PDF report for an uploaded analysis session."""
    try:
        pdf_bytes = generate_pdf_report(session_id)
    except ValueError as exc:
        status_code = 404 if "not found" in str(exc) else 400
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="plagiarism-report-{session_id}.pdf"'
        },
    )
