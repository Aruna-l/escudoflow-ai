from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.services.dashboard import scan_stats_service
from app.services.report import report_service

MODEL_VALIDATION_ACCURACY = 99.4


SEVERITY_ORDER = ["Safe", "Low", "Suspicious", "High", "Critical"]

VECTOR_CATEGORY_RULES = [
    ("BEC", "BEC"),
    ("Cloned Login", "Brand Impersonation"),
    ("Malicious File", "Malware"),
    ("Malicious URL", "Credential Phishing"),
    ("Phishing", "Credential Phishing"),
]

def _pct_delta(current: float, previous: float) -> Optional[float]:
    if not previous:
        return None
    return round((current - previous) / previous * 100, 1)

def _parse_ts(created_at: str) -> datetime:
    # createdAt is "%Y-%m-%d %H:%M UTC"
    return datetime.strptime(created_at.replace(" UTC", ""), "%Y-%m-%d %H:%M")


def _classify_category(vector: str) -> str:
    for needle, category in VECTOR_CATEGORY_RULES:
        if needle in vector:
            return category
    return "Other"


def _all_reports(days: int = None) -> List[dict]:
    reports = report_service.list_reports_full()
    if days is None:
        return reports
    cutoff = datetime.utcnow() - timedelta(days=days)
    return [r for r in reports if _parse_ts(r["createdAt"]) >= cutoff]


# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------
def compute_kpis() -> Dict[str, Any]:
    now = datetime.utcnow()
    all_reports = _all_reports()

    day_ago = now - timedelta(hours=24)
    two_days_ago = now - timedelta(hours=48)

    threats_today = len([r for r in all_reports if _parse_ts(r["createdAt"]) >= day_ago])
    threats_prev_day = len([
        r for r in all_reports if two_days_ago <= _parse_ts(r["createdAt"]) < day_ago
    ])

    critical_today = len([
        r for r in all_reports
        if r["severity"] == "Critical" and _parse_ts(r["createdAt"]) >= day_ago
    ])
    critical_prev_day = len([
        r for r in all_reports
        if r["severity"] == "Critical" and two_days_ago <= _parse_ts(r["createdAt"]) < day_ago
    ])

    investigations_now = len(all_reports)
    investigations_24h_ago = len([r for r in all_reports if _parse_ts(r["createdAt"]) <= day_ago])

    blocked_now = len([r for r in all_reports if r["status"] == "Blocked"])
    blocked_24h_ago = len([
        r for r in all_reports if r["status"] == "Blocked" and _parse_ts(r["createdAt"]) <= day_ago
    ])

    safe_now = scan_stats_service.safe_scans_up_to(now)
    safe_24h_ago = scan_stats_service.safe_scans_up_to(day_ago)

    return {
        "threatsToday": threats_today,
        "threatsTodayDeltaPct": _pct_delta(threats_today, threats_prev_day),
        "investigations": investigations_now,
        "investigationsDeltaPct": _pct_delta(investigations_now, investigations_24h_ago),
        "criticalAlerts": critical_today,
        "criticalAlertsDeltaPct": _pct_delta(critical_today, critical_prev_day),
        "blockedAttacks": blocked_now,
        "blockedAttacksDeltaPct": _pct_delta(blocked_now, blocked_24h_ago),
        "safeMessages": safe_now,
        "safeMessagesDeltaPct": _pct_delta(safe_now, safe_24h_ago),
        "detectionAccuracy": MODEL_VALIDATION_ACCURACY,
        "riskLevel": "Critical" if critical_today > 0 else ("Elevated" if threats_today > 5 else "Normal"),
        "avgInvestigationTimeSeconds": 1.8,
    }


# ---------------------------------------------------------------------------
# Threat trend (14 days): detected vs blocked
# ---------------------------------------------------------------------------
def compute_threat_trend(days: int = 14) -> List[Dict[str, Any]]:
    reports = _all_reports(days=days)
    buckets: Dict[str, Dict[str, int]] = defaultdict(lambda: {"threats": 0, "blocked": 0})

    for r in reports:
        day_key = _parse_ts(r["createdAt"]).strftime("%Y-%m-%d")
        buckets[day_key]["threats"] += 1
        if r["status"] == "Blocked":
            buckets[day_key]["blocked"] += 1

    ordered = []
    for i in range(days - 1, -1, -1):
        day = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        b = buckets.get(day, {"threats": 0, "blocked": 0})
        ordered.append({"day": day, "threats": b["threats"], "blocked": b["blocked"]})
    return ordered


# ---------------------------------------------------------------------------
# Attack categories
# ---------------------------------------------------------------------------
def compute_attack_categories() -> List[Dict[str, Any]]:
    reports = _all_reports()
    if not reports:
        return []
    counts: Dict[str, int] = defaultdict(int)
    for r in reports:
        vector = (r.get("threatOverview") or {}).get("vector", "Unclassified")
        counts[_classify_category(vector)] += 1

    total = sum(counts.values())
    return [
        {"name": name, "value": round(count / total * 100)}
        for name, count in sorted(counts.items(), key=lambda x: -x[1])
    ]


# ---------------------------------------------------------------------------
# Daily investigations (last 7 days): investigations vs resolved
# ---------------------------------------------------------------------------
def compute_daily_investigations() -> List[Dict[str, Any]]:
    reports = _all_reports(days=7)
    buckets: Dict[str, Dict[str, int]] = defaultdict(lambda: {"investigations": 0, "resolved": 0})

    for r in reports:
        day_label = _parse_ts(r["createdAt"]).strftime("%a")
        buckets[day_label]["investigations"] += 1
        if r["status"] in ("Resolved", "Blocked"):
            buckets[day_label]["resolved"] += 1

    order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return [{"day": d, **buckets.get(d, {"investigations": 0, "resolved": 0})} for d in order]


# ---------------------------------------------------------------------------
# Risk distribution
# ---------------------------------------------------------------------------
def compute_risk_distribution() -> List[Dict[str, Any]]:
    reports = _all_reports(days=30)
    if not reports:
        return []
    counts: Dict[str, int] = defaultdict(int)
    for r in reports:
        counts[r.get("severity", "Safe")] += 1
    total = sum(counts.values())
    return [
        {"name": level, "value": round(counts.get(level, 0) / total * 100)}
        for level in SEVERITY_ORDER
        if counts.get(level, 0) > 0
    ]


# ---------------------------------------------------------------------------
# Threat sources
# ---------------------------------------------------------------------------
def compute_threat_sources(limit: int = 5) -> List[Dict[str, Any]]:
    reports = _all_reports()
    counts: Dict[str, int] = defaultdict(int)
    for r in reports:
        country = r.get("sourceCountry", "Unknown")
        if country != "Unknown":
            counts[country] += 1
    ranked = sorted(counts.items(), key=lambda x: -x[1])[:limit]
    return [{"country": c, "value": v} for c, v in ranked]


# ---------------------------------------------------------------------------
# Recent investigations table
# ---------------------------------------------------------------------------
def compute_recent_investigations(limit: int = 10) -> List[Dict[str, Any]]:
    reports = sorted(_all_reports(), key=lambda r: r["createdAt"], reverse=True)[:limit]
    rows = []
    for r in reports:
        overview = r.get("threatOverview") or {}
        domain_ioc = next((i["value"] for i in r.get("iocs", []) if i["type"] == "Domain"), "Unknown")
        rows.append({
            "id": r["id"],
            "date": r["createdAt"],
            "source": domain_ioc,
            "target": overview.get("target", "Unknown"),
            "threatType": overview.get("vector", "Unclassified"),
            "riskScore": r.get("riskScore", 0),
            "status": r["status"],
        })
    return rows


# ---------------------------------------------------------------------------
# Alert feed — recent Critical/High reports
# ---------------------------------------------------------------------------
def compute_alerts(limit: int = 6) -> List[Dict[str, Any]]:
    reports = [r for r in _all_reports() if r["severity"] in ("Critical", "High")]
    reports = sorted(reports, key=lambda r: r["createdAt"], reverse=True)[:limit]
    now = datetime.utcnow()
    alerts = []
    for r in reports:
        minutes_ago = int((now - _parse_ts(r["createdAt"])).total_seconds() // 60)
        time_label = f"{minutes_ago}m ago" if minutes_ago < 60 else f"{minutes_ago // 60}h ago"
        alerts.append({
            "id": r["id"],
            "severity": r["severity"].lower(),
            "time": time_label,
            "title": r["title"],
            "source": (r.get("threatOverview") or {}).get("vector", "Unclassified"),
        })
    return alerts


# ---------------------------------------------------------------------------
# AI findings + recommendations
# ---------------------------------------------------------------------------
def compute_insights() -> Dict[str, Any]:
    reports = _all_reports(days=2)
    findings = []

    clusters: Dict[tuple, List[dict]] = defaultdict(list)
    for r in reports:
        overview = r.get("threatOverview") or {}
        key = (overview.get("vector", "Unclassified"), overview.get("target", "Unknown"))
        clusters[key].append(r)

    for (vector, target), items in sorted(clusters.items(), key=lambda x: -len(x[1]))[:3]:
        if len(items) < 2:
            continue
        avg_risk = round(sum(i["riskScore"] for i in items) / len(items))
        findings.append({
            "title": f"{vector} cluster targeting {target}",
            "score": avg_risk,
            "detail": f"{len(items)} investigations share the same vector and target in the last 48h.",
        })

    recommendations = []
    blocked_count = len([r for r in reports if r["status"] == "Blocked"])
    if blocked_count:
        recommendations.append(f"{blocked_count} attacks were auto-blocked in the last 48h — review for pattern reuse.")
    critical_targets = {(r.get("threatOverview") or {}).get("target") for r in reports if r["severity"] == "Critical"}
    critical_targets.discard(None)
    if critical_targets:
        recommendations.append(
            f"Enforce MFA for: {', '.join(sorted(critical_targets)[:5])} — flagged in critical-severity investigations."
        )
    if not recommendations:
        recommendations.append("No high-severity patterns in the last 48h — no action required.")

    return {"findings": findings, "recommendations": recommendations}