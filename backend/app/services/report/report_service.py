import csv
import io
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from app.services.dashboard import scan_stats_service
from app.core.constants import RISK_THRESHOLDS
from app.schemas.report import (
    ReportGenerateRequest,
    ReportResponse,
    EvidenceItem,
    IOCItem,
    ThreatOverview,
    TimelineEvent,
)

# ---------------------------------------------------------------------------
# In-memory stores.
#   _REPORTS   -> id -> fully fused report dict (both manual /generate reports
#                 and the rolling per-session "live" report live here)
#   _INCIDENTS -> session_id -> raw per-source inputs + timestamps, used to
#                 build the rolling report for that session/tab.
# ---------------------------------------------------------------------------
_REPORTS: Dict[str, dict] = {}
_INCIDENTS: Dict[str, dict] = {}
_VALID_STATUSES = {"Investigating", "Blocked", "Escalated", "Resolved"}
_STATUS_OVERRIDES: Dict[str, str] = {}
SOURCE_TYPES = ("email", "url", "attachment", "threat", "visual")

# A source older than this is treated as unrelated to what's being
# investigated right now and excluded from fusion (but not deleted —
# touching that source again just makes it fresh again).
STALE_AFTER_MINUTES = 30

_DANGEROUS_VERDICTS = {"dangerous", "phishing", "malicious", "fake", "spoofed", "clone"}


def _as_dict(obj) -> dict:
    """Normalize a route's return value (dict, or Pydantic model) into a plain dict."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    return dict(obj)


# ---------------------------------------------------------------------------
# ID / timestamp helpers
# ---------------------------------------------------------------------------
def _generate_report_id() -> str:
    while True:
        candidate = f"AF-INC-{datetime.utcnow().year}-{random.randint(10000, 99999)}"
        if candidate not in _REPORTS:
            return candidate


def _now_str() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")


# ---------------------------------------------------------------------------
# Risk score + severity + confidence fusion
# ---------------------------------------------------------------------------
_REPUTATION_RISK = {"malicious": 90, "suspicious": 60, "clean": 5}
def _single_source_risk(source_type: str, data: dict) -> Optional[int]:
    """Best-effort risk score for one raw source result, used only to
    classify a scan as malicious/clean for stats — not part of report fusion."""
    if source_type == "email":
        return _get_first(data, "riskScore", "overallRisk")
    if source_type == "url":
        return _get_first(data, "risk_score", "overallRisk")
    if source_type == "attachment":
        return data.get("riskScore")
    if source_type == "threat":
        reputation = str(data.get("reputation", "")).lower()
        return _REPUTATION_RISK.get(reputation, 50)
    if source_type == "visual":
        return data.get("overallRisk")
    return None


def _score_to_severity(score: int) -> str:
    for threshold, label in RISK_THRESHOLDS:
        if score >= threshold:
            return label.capitalize()
    return "Safe"


def _get_first(d: Optional[dict], *keys, default=None):
    if not d:
        return default
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default


def _is_dangerous_verdict(verdict: Optional[str]) -> bool:
    return bool(verdict) and verdict.strip().lower() in _DANGEROUS_VERDICTS


def _compute_risk_and_confidence(
    email: Optional[dict], url: Optional[dict], threat: Optional[dict],
    attachment: Optional[dict], visual: Optional[dict],
) -> Tuple[int, int]:
    risk_signals: List[float] = []
    confidence_signals: List[float] = []

    if email:
        risk = _get_first(email, "riskScore", "overallRisk")
        if risk is not None:
            risk_signals.append(risk)
        prob = email.get("phishingProbability")
        if prob is not None:
            confidence_signals.append(prob * 100)

    if url:
        risk = _get_first(url, "risk_score", "overallRisk")
        if risk is not None:
            risk_signals.append(risk)
        conf = _get_first(url, "confidence")
        if conf is not None:
            confidence_signals.append(conf)
        brand = (url.get("brand_similarity") or {}).get("brandSimilarity")
        if brand:
            confidence_signals.append(brand)

    if attachment:
        risk = attachment.get("riskScore")
        if risk is not None:
            risk_signals.append(risk)
            confidence_signals.append(risk)

    if threat:
        reputation = str(threat.get("reputation", "")).lower()
        risk_signals.append(_REPUTATION_RISK.get(reputation, 50))
        if threat.get("confidence") is not None:
            confidence_signals.append(threat["confidence"])

    if visual:
        # Real VisualResponse shape: overallRisk (0-100 int), verdict,
        # detectedBrand (flat), similarity{visual,logo,color,layout} (0-1
        # floats), logo{detected,brand,confidence}. No nested "brand" object,
        # no "fakeLoginDetected" boolean — that badge on the frontend page
        # is currently hardcoded JSX, not driven by response data.
        overall_risk = visual.get("overallRisk")
        if overall_risk is not None:
            risk_signals.append(overall_risk)
            confidence_signals.append(overall_risk)
        logo_conf = (visual.get("logo") or {}).get("confidence")
        if logo_conf:
            confidence_signals.append(logo_conf)

    risk_score = round(max(risk_signals)) if risk_signals else 50
    confidence = round(sum(confidence_signals) / len(confidence_signals)) if confidence_signals else 75
    return min(risk_score, 100), min(confidence, 100)


# ---------------------------------------------------------------------------
# IOC extraction
# ---------------------------------------------------------------------------
def _domain_from_email_addr(addr: Optional[str]) -> Optional[str]:
    return addr.split("@")[-1] if addr and "@" in addr else None


def _domain_from_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    stripped = url.split("//")[-1]
    return stripped.split("/")[0]

# ---------------------------------------------------------------------------
# Country extraction — module-level, not redefined per-call
# ---------------------------------------------------------------------------
def _extract_country(url: Optional[dict], threat: Optional[dict]) -> str:
    if url and (url.get("whois") or {}).get("country") not in (None, "Unknown"):
        return url["whois"]["country"]
    if threat:
        for feed in threat.get("feeds", []):
            country = (feed.get("raw") or {}).get("country")
            if country:
                return country
    return "Unknown"

def _build_iocs(
    email: Optional[dict], url: Optional[dict], threat: Optional[dict],
    attachment: Optional[dict], visual: Optional[dict],
) -> List[IOCItem]:
    iocs: List[Tuple[str, str]] = []

    if email:
        from_domain = _domain_from_email_addr(email.get("from_email"))
        if from_domain:
            iocs.append(("Domain", from_domain))
        reply_to = email.get("reply_to")
        if reply_to:
            iocs.append(("Email", reply_to))

    if url:
        raw_url = url.get("analyzed_url") or url.get("url")
        domain = _domain_from_url(raw_url)
        if domain:
            iocs.append(("Domain", domain))

        ip = (url.get("hosting") or {}).get("ip")
        if ip and ip != "Unknown":
            iocs.append(("IPv4", ip))

        for a_ip in (url.get("dns") or {}).get("a_records", []):
            iocs.append(("IPv4", a_ip))

    if threat and threat.get("ioc"):
        ioc_type = threat.get("type", "IOC")
        type_label = "IPv4" if str(ioc_type).upper() in ("IP", "IPV4") else ioc_type
        iocs.append((type_label, threat["ioc"]))

    if attachment and attachment.get("sha256"):
        iocs.append(("SHA256", attachment["sha256"]))

    if visual:
        # "targetUrl" isn't part of VisualResponse — the route merges the
        # form's `url` field into this dict as "targetUrl" before calling
        # update_incident_source(), same pattern as url.py's "analyzed_url".
        domain = _domain_from_url(visual.get("targetUrl"))
        if domain:
            iocs.append(("Domain", domain))
        qr_data = (visual.get("qr") or {}).get("data")
        if qr_data and (qr_data.startswith("http://") or qr_data.startswith("https://")):
            iocs.append(("URL", qr_data))

    seen = set()
    deduped: List[IOCItem] = []
    for t, v in iocs:
        key = (t, v)
        if key not in seen:
            seen.add(key)
            deduped.append(IOCItem(type=t, value=v))
    return deduped


# ---------------------------------------------------------------------------
# Timeline
# ---------------------------------------------------------------------------
def _build_timeline(
    email: Optional[dict], url: Optional[dict], threat: Optional[dict],
    attachment: Optional[dict], visual: Optional[dict], severity: str,
) -> List[TimelineEvent]:
    steps: List[str] = []

    if email:
        steps.append("Inbound message received by mail gateway")
        prob = email.get("phishingProbability")
        steps.append(
            f"EscudoFlow Email Intelligence scored {prob:.2f} phishing" if prob is not None
            else "EscudoFlow Email Intelligence analysis completed"
        )
        if email.get("bec"):
            steps.append("BEC classifier confirmed CEO/executive impersonation")

    if url:
        prediction = _get_first(url, "prediction", "verdict", default="analyzed")
        steps.append(f"URL Intelligence flagged linked URL as {prediction}")

    if visual:
        brand = visual.get("detectedBrand")
        verdict = visual.get("verdict")
        if brand and _is_dangerous_verdict(verdict):
            steps.append(f"Visual Intelligence detected cloned {brand} login page")
        else:
            steps.append("Visual Intelligence analysis completed")

    if attachment:
        name = attachment.get("fileName", "attachment")
        steps.append(f"Attachment Intelligence analyzed {name} for malicious content")

    if threat:
        reputation = threat.get("reputation", "unknown")
        steps.append(f"Threat Intelligence correlated IOC — reputation: {reputation}")

    if severity in ("Critical", "High"):
        steps.append("Message quarantined; recipient notified")
    else:
        steps.append("Findings logged for analyst review")

    steps.append("Incident report generated automatically")

    now = datetime.utcnow()
    n = len(steps)
    timeline: List[TimelineEvent] = []
    for i, event in enumerate(steps):
        t = now - timedelta(minutes=(n - i - 1))
        timeline.append(TimelineEvent(t=t.strftime("%H:%M"), event=event))
    return timeline


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------
def _build_recommendations(
    email: Optional[dict], url: Optional[dict], threat: Optional[dict],
    attachment: Optional[dict], visual: Optional[dict],
) -> List[str]:
    recs: List[str] = []

    if email:
        email_recs = (email.get("aiExplanation") or {}).get("recommendations")
        if email_recs:
            recs.extend(email_recs)
    if url and (url.get("ai_explanation") or {}).get("recommendations"):
        recs.extend(url["ai_explanation"]["recommendations"])
    if attachment and attachment.get("recommendation"):
        recs.append(attachment["recommendation"])
    if threat and threat.get("actions"):
        recs.extend(threat["actions"])
    if visual and visual.get("recommendations"):
        recs.extend(visual["recommendations"])

    if not recs:
        recs.append("Review findings with a senior analyst before closing this incident")

    seen = set()
    deduped = []
    for r in recs:
        if r not in seen:
            seen.add(r)
            deduped.append(r)
    return deduped


# ---------------------------------------------------------------------------
# Executive summary + threat overview
# ---------------------------------------------------------------------------
def _build_executive_summary(
    email: Optional[dict], url: Optional[dict], threat: Optional[dict],
    attachment: Optional[dict], visual: Optional[dict], target: Optional[str],
) -> str:
    parts: List[str] = []
    today = datetime.utcnow().strftime("%Y-%m-%d")

    if email and email.get("bec"):
        entities = email.get("entities") or {}
        person = (entities.get("person") or ["an executive"])[0]
        amount = (entities.get("amount") or [None])[0]
        parts.append(
            f"On {today}, EscudoFlow AI detected a targeted Business Email Compromise "
            f"attempt impersonating {person}"
            + (f", requesting a transfer of {amount}" if amount else "")
            + (f" against {target}" if target else "") + "."
        )
    elif email:
        parts.append(
            f"On {today}, EscudoFlow AI flagged a phishing email"
            + (f" targeting {target}" if target else "") + "."
        )

    if url:
        prediction = _get_first(url, "prediction", "verdict")
        raw_url = url.get("analyzed_url") or url.get("url")
        if prediction in ("Phishing", "Dangerous") and raw_url:
            parts.append(f"The message referenced a malicious URL ({raw_url}).")

    if visual:
        brand = visual.get("detectedBrand")
        verdict = visual.get("verdict")
        if brand and _is_dangerous_verdict(verdict):
            parts.append(
                f"Visual analysis confirmed a cloned {brand} login page designed to harvest credentials."
            )

    if attachment:
        parts.append(
            f"An attached file ({attachment.get('fileName', 'unknown')}) was found to be malicious."
        )

    if threat and threat.get("reputation", "").lower() == "malicious":
        parts.append(
            f"Associated infrastructure was linked to known campaign "
            f"'{threat.get('knownCampaign', 'unclassified activity')}'."
        )

    if not parts:
        parts.append(
            f"On {today}, EscudoFlow AI generated this report; no source analyses "
            "were attached, so findings should be added manually."
        )

    parts.append("No further user interaction occurred beyond the point of detection.")
    return " ".join(parts)


def _build_threat_overview(
    email: Optional[dict], url: Optional[dict], attachment: Optional[dict],
    visual: Optional[dict], target: Optional[str],
) -> ThreatOverview:
    vectors = []
    if email:
        vectors.append("Email — BEC" if email.get("bec") else "Email — Phishing")
    if url:
        vectors.append("Web — Malicious URL")
    if attachment:
        vectors.append("Attachment — Malicious File")
    if visual and _is_dangerous_verdict(visual.get("verdict")):
        vectors.append("Web — Cloned Login Page")
    vector = " + ".join(vectors) if vectors else "Unclassified"

    resolved_target = target or (email.get("to") if email else None) or "Unknown"

    impact = "No direct financial impact identified"
    if email:
        entities = email.get("entities") or {}
        amount = (entities.get("amount") or [None])[0]
        if amount:
            impact = f"{amount} attempted"

    return ThreatOverview(vector=vector, target=resolved_target, impact=impact)


# ---------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------
def _build_evidence(
    email: Optional[dict], url: Optional[dict], threat: Optional[dict],
    attachment: Optional[dict], visual: Optional[dict],
) -> List[EvidenceItem]:
    evidence: List[EvidenceItem] = []
    if email:
        evidence.append(EvidenceItem(filename="raw-message.eml", sourceType="email"))
        evidence.append(EvidenceItem(filename="header-analysis.json", sourceType="email"))
    if url:
        evidence.append(EvidenceItem(filename="url-analysis.json", sourceType="url"))
    if visual:
        evidence.append(EvidenceItem(filename="screenshot-clone.png", sourceType="visual"))
    if attachment:
        evidence.append(EvidenceItem(
            filename=f"{attachment.get('fileName', 'attachment')}.analysis.json",
            sourceType="attachment",
        ))
        evidence.append(EvidenceItem(filename="behavior-trace.json", sourceType="attachment"))
    if threat:
        evidence.append(EvidenceItem(filename="threat-intel.json", sourceType="threat"))
    return evidence


# ---------------------------------------------------------------------------
# Core fuse (shared by manual generate + rolling per-session incident)
# ---------------------------------------------------------------------------
def _fuse(
    report_id: str, created_at: str, analyst: str, target: Optional[str],
    notes: Optional[str],
    email: Optional[dict], url: Optional[dict], threat: Optional[dict],
    attachment: Optional[dict], visual: Optional[dict],
) -> dict:
    risk_score, confidence = _compute_risk_and_confidence(email, url, threat, attachment, visual)
    severity = _score_to_severity(risk_score)
    status = _STATUS_OVERRIDES.get(report_id) or _default_status(severity, risk_score)

    iocs = _build_iocs(email, url, threat, attachment, visual)
    source_country = _extract_country(url, threat)
    timeline = _build_timeline(email, url, threat, attachment, visual, severity)
    recommendations = _build_recommendations(email, url, threat, attachment, visual)
    executive_summary = _build_executive_summary(email, url, threat, attachment, visual, target)
    threat_overview = _build_threat_overview(email, url, attachment, visual, target)
    evidence = _build_evidence(email, url, threat, attachment, visual)

    title = (
        f"{threat_overview.vector} Attempt — {threat_overview.target}"
        if threat_overview.vector != "Unclassified" else "Security Incident Report"
    )

    report = ReportResponse(
        id=report_id,
        title=title,
        createdAt=created_at,
        analyst=analyst,
        severity=severity,
        riskScore=risk_score,
        confidence=confidence,
        executiveSummary=executive_summary,
        threatOverview=threat_overview,
        iocs=iocs,
        timeline=timeline,
        recommendations=recommendations,
        evidence=evidence,
        analystNotes=notes,
        sourceCountry=source_country,
        status=status,
    )
    return report.model_dump()

# ---------------------------------------------------------------------------
# Public API — manual generation (POST /report/generate), unrelated to
# sessions — always makes a standalone, permanent report.
# ---------------------------------------------------------------------------
def generate_report(payload: ReportGenerateRequest) -> dict:
    report_dict = _fuse(
        report_id=_generate_report_id(),
        created_at=_now_str(),
        analyst=payload.analyst or "EscudoFlow AI",
        target=payload.target,
        notes=payload.notes,
        email=payload.email, url=payload.url, threat=payload.threat,
        attachment=payload.attachment, visual=payload.visual,
    )
    _REPORTS[report_dict["id"]] = report_dict
    return report_dict


def get_report(report_id: str) -> Optional[dict]:
    return _REPORTS.get(report_id)


def list_reports() -> List[dict]:
    items = sorted(_REPORTS.values(), key=lambda r: r["createdAt"], reverse=True)
    return [
        {
            "id": r["id"], "title": r["title"], "createdAt": r["createdAt"],
            "analyst": r["analyst"], "severity": r["severity"], "riskScore": r["riskScore"],
            "status": r["status"],
        }
        for r in items
    ]
def list_reports_full() -> List[dict]:
    """Full fused report dicts — used by dashboard aggregation, unlike the
    trimmed ReportListItem from list_reports()."""
    return list(_REPORTS.values())

def update_status(report_id: str, status: str) -> Optional[dict]:
    if status not in _VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Must be one of {sorted(_VALID_STATUSES)}")
    report = _REPORTS.get(report_id)
    if not report:
        return None
    _STATUS_OVERRIDES[report_id] = status
    report["status"] = status
    return report


# ---------------------------------------------------------------------------
# Public API — rolling per-session incident (auto-generated from live
# analyses). Keyed by session_id so concurrent tabs/users never collide.
# ---------------------------------------------------------------------------
def _get_incident(session_id: str) -> dict:
    if session_id not in _INCIDENTS:
        _INCIDENTS[session_id] = {
            "sources": {k: None for k in SOURCE_TYPES},  # each: {"data": dict, "ts": datetime} | None
            "target": None,
            "notes": None,
            "report_id": None,
        }
    return _INCIDENTS[session_id]


def _active_sources(incident: dict) -> Dict[str, Optional[dict]]:
    """Sources touched more than STALE_AFTER_MINUTES ago are excluded from
    fusion — an old unrelated test won't get stitched into a fresh report."""
    now = datetime.utcnow()
    active: Dict[str, Optional[dict]] = {}
    for source_type, entry in incident["sources"].items():
        if entry is None:
            active[source_type] = None
            continue
        age = now - entry["ts"]
        active[source_type] = entry["data"] if age <= timedelta(minutes=STALE_AFTER_MINUTES) else None
    return active


def update_incident_source(session_id: str, source_type: str, data, target: Optional[str] = None) -> dict:
    if source_type not in SOURCE_TYPES:
        raise ValueError(f"Unknown source_type: {source_type}")

    normalized = _as_dict(data)
    incident = _get_incident(session_id)
    incident["sources"][source_type] = {"data": normalized, "ts": datetime.utcnow()}
    if target:
        incident["target"] = target
    risk = _single_source_risk(source_type, normalized)
    if risk is not None:
        scan_stats_service.record_scan(source_type, is_malicious=_score_to_severity(risk) != "Safe")

    active = _active_sources(incident)
    report_id = incident["report_id"] or f"AF-INC-LIVE-{session_id[:8]}"
    incident["report_id"] = report_id

    existing = _REPORTS.get(report_id)
    created_at = existing["createdAt"] if existing else _now_str()

    report_dict = _fuse(
        report_id=report_id,
        created_at=created_at,
        analyst="EscudoFlow AI",
        target=incident.get("target"),
        notes=incident.get("notes"),
        email=active["email"], url=active["url"], threat=active["threat"],
        attachment=active["attachment"], visual=active["visual"],
    )
    _REPORTS[report_id] = report_dict
    return report_dict


def get_latest_report(session_id: str) -> Optional[dict]:
    """
    Re-fuses on every read (not just on write) so that staleness expiry
    takes effect even if the user just sits on the Reports page — a source
    that ages past 30 minutes will visibly drop out next refresh.
    """
    incident = _INCIDENTS.get(session_id)
    if not incident or not incident.get("report_id"):
        return None

    active = _active_sources(incident)
    if not any(active.values()):
        return None  # everything expired — nothing live to show

    report_id = incident["report_id"]
    existing = _REPORTS.get(report_id)
    created_at = existing["createdAt"] if existing else _now_str()
    notes = (existing or {}).get("analystNotes") or incident.get("notes")

    report_dict = _fuse(
        report_id=report_id,
        created_at=created_at,
        analyst="EscudoFlow AI",
        target=incident.get("target"),
        notes=notes,
        email=active["email"], url=active["url"], threat=active["threat"],
        attachment=active["attachment"], visual=active["visual"],
    )
    _REPORTS[report_id] = report_dict
    return report_dict


def reset_incident(session_id: str) -> None:
    incident = _INCIDENTS.pop(session_id, None)
    if incident and incident.get("report_id"):
        report_id = incident["report_id"]
        _REPORTS.pop(report_id, None)
        _STATUS_OVERRIDES.pop(report_id, None)


# ---------------------------------------------------------------------------
# Exports (unchanged — operate on whatever report_id is passed, session-agnostic)
# ---------------------------------------------------------------------------
def export_json(report_id: str) -> Optional[dict]:
    return _REPORTS.get(report_id)


def export_csv(report_id: str) -> Optional[str]:
    report = _REPORTS.get(report_id)
    if not report:
        return None

    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow(["Report ID", report["id"]])
    writer.writerow(["Title", report["title"]])
    writer.writerow(["Created At", report["createdAt"]])
    writer.writerow(["Analyst", report["analyst"]])
    writer.writerow(["Severity", report["severity"]])
    writer.writerow(["Risk Score", report["riskScore"]])
    writer.writerow(["Confidence", report["confidence"]])
    writer.writerow([])

    writer.writerow(["Executive Summary"])
    writer.writerow([report["executiveSummary"]])
    writer.writerow([])

    writer.writerow(["IOC Type", "IOC Value"])
    for ioc in report["iocs"]:
        writer.writerow([ioc["type"], ioc["value"]])
    writer.writerow([])

    writer.writerow(["Timeline (UTC)", "Event"])
    for step in report["timeline"]:
        writer.writerow([step["t"], step["event"]])
    writer.writerow([])

    writer.writerow(["Recommendations"])
    for rec in report["recommendations"]:
        writer.writerow([rec])

    return buffer.getvalue()


def export_pdf(report_id: str) -> Optional[bytes]:
    report = _REPORTS.get(report_id)
    if not report:
        return None

    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER
    y = height - 1 * inch

    def line(text: str, size: int = 10, gap: float = 14, bold: bool = False):
        nonlocal y
        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(1 * inch, y, text[:110])
        y -= gap

    line(report["title"], size=16, bold=True, gap=22)
    line(f"{report['id']}  |  {report['createdAt']}  |  Analyst: {report['analyst']}")
    line(f"Severity: {report['severity']}   Risk Score: {report['riskScore']}   Confidence: {report['confidence']}%")
    y -= 10

    line("Executive Summary", size=12, bold=True, gap=16)
    for chunk in [report["executiveSummary"][i:i+95] for i in range(0, len(report["executiveSummary"]), 95)]:
        line(chunk)
    y -= 10

    line("Indicators of Compromise", size=12, bold=True, gap=16)
    for ioc in report["iocs"]:
        line(f"{ioc['type']}: {ioc['value']}")
    y -= 10

    line("Timeline", size=12, bold=True, gap=16)
    for step in report["timeline"]:
        line(f"{step['t']} UTC — {step['event']}")
    y -= 10

    line("Recommendations", size=12, bold=True, gap=16)
    for rec in report["recommendations"]:
        line(f"- {rec}")

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
def _default_status(severity: str, risk_score: int) -> str:
    if severity == "Critical" and risk_score >= 95:
        return "Escalated"
    if severity in ("Critical", "High") and risk_score >= 80:
        return "Blocked"
    if severity in ("Critical", "High", "Suspicious"):
        return "Investigating"
    return "Resolved"