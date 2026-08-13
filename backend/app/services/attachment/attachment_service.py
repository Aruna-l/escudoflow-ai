import re

from app.core.constants import SUSPICIOUS_EXTENSIONS, OFFICE_EXTENSIONS, RAW_SCRIPT_EXTENSIONS, FILE_TYPE_LABELS
from app.schemas.attachment import AttachmentAnalysisResponse
from app.services.attachment.hash_utils import compute_sha256
from app.services.attachment.macro_analyzer import extract_vba_code, has_macro_container
from app.services.attachment.script_analyzer import analyze_vba_code, count_suspicious_executables
from app.services.attachment.risk_engine import compute_risk, build_recommendation


def analyze_attachments(email_body: str):
    """
    Detect filenames mentioned inside an email body
    and assign a simple risk score.

    (Unchanged from your existing implementation — used by the Email
    Intelligence flow to flag attachment names referenced in message text.)
    """
    pattern = r"\b[\w\-]+\.(?:exe|dll|bat|cmd|scr|js|vbs|ps1|jar|zip|rar|7z|iso|docm|xlsm|pptm|doc|xls|ppt|pdf)\b"

    files = re.findall(pattern, email_body, flags=re.IGNORECASE)

    results = []

    for file in files:
        extension = "." + file.split(".")[-1].lower()

        risk = SUSPICIOUS_EXTENSIONS.get(extension, 20)

        results.append(
            {
                "filename": file,
                "risk_score": risk,
            }
        )

    return results


def _format_size(num_bytes: int) -> str:
    kb = num_bytes / 1024
    if kb < 1024:
        return f"{round(kb)} KB"
    return f"{round(kb / 1024, 1)} MB"


def analyze_attachment_file(filename: str, data: bytes) -> AttachmentAnalysisResponse:
    """
    Full static analysis of an uploaded attachment: macro detection,
    embedded-script inspection, suspicious-executable detection, and an
    aggregate risk score + recommendation. This powers the "Drop a file
    to analyze" upload flow on the Attachment Intelligence page.

    Returns a response shaped to match ATTACHMENT_ANALYSIS_MOCK in the
    frontend 1:1 (flat, camelCase) so the frontend can swap the mock for
    this response with no reshaping.
    """
    extension = ("." + filename.rsplit(".", 1)[-1].lower()) if "." in filename else ""
    sha256 = compute_sha256(data)

    macros_detected = False
    script_source = ""

    if extension in OFFICE_EXTENSIONS:
        macros_detected = has_macro_container(filename, data)
        if macros_detected:
            script_source = extract_vba_code(filename, data)
    elif extension in RAW_SCRIPT_EXTENSIONS:
        # Not an Office macro — the file itself IS the script. Scan its
        # own text content with the same pattern matcher.
        script_source = data.decode("utf-8", errors="ignore")

    threat_items, embedded_scripts_count = analyze_vba_code(script_source)
    suspicious_exec_count = count_suspicious_executables(filename, data, extension)

    risk_score, risk_label = compute_risk(
        extension=extension,
        macros_detected=macros_detected,
        threat_items=threat_items,
        suspicious_exec_count=suspicious_exec_count,
    )

    recommendation = build_recommendation(risk_label, threat_items)

    file_type_label = FILE_TYPE_LABELS.get(extension, (extension.lstrip(".").upper() or "Unknown"))

    return AttachmentAnalysisResponse(
        riskScore=risk_score,
        riskLabel=risk_label,
        fileName=filename,
        fileType=file_type_label,
        size=_format_size(len(data)),
        macros=macros_detected,
        embeddedScripts=embedded_scripts_count,
        suspiciousExecutables=suspicious_exec_count,
        sha256=sha256,
        threats=threat_items,
        recommendation=recommendation,
    )
