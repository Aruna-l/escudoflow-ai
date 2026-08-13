from typing import List, Tuple

from app.core.constants import SUSPICIOUS_EXTENSIONS, SEVERITY_WEIGHTS, RISK_THRESHOLDS
from app.schemas.attachment import ThreatItem


def score_to_label(score: int) -> str:
    for threshold, label in RISK_THRESHOLDS:
        if score >= threshold:
            return label
    return "LOW"


def compute_risk(
    extension: str,
    macros_detected: bool,
    threat_items: List[ThreatItem],
    suspicious_exec_count: int,
) -> Tuple[int, str]:
    score = SUSPICIOUS_EXTENSIONS.get(extension.lower(), 20)

    if macros_detected:
        score += 20

    for item in threat_items:
        score += SEVERITY_WEIGHTS.get(item.severity, 5)

    # Cap the executable contribution so a zip stuffed with 50 files
    # doesn't trivially max the score out on its own.
    score += min(suspicious_exec_count, 3) * 10

    score = max(0, min(100, score))
    return score, score_to_label(score)


def build_recommendation(label: str, threat_items: List[ThreatItem]) -> str:
    has_callback = any(
        "domain" in item.name.lower() or "remote" in item.name.lower()
        for item in threat_items
    )

    if label == "critical":
        if has_callback:
            return "Quarantine the file, block the callback domain, and audit any host that opened it."
        return "Quarantine the file immediately and audit any host that opened it."
    if label == "high":
        return "Quarantine the file pending manual review and avoid opening it on a production host."
    if label == "suspicious":
        return "Treat this attachment with caution — open it only inside a sandboxed environment before forwarding."
    if label == "low":
        return "Low risk detected. Review the flagged indicators before forwarding internally."
    return "No significant threats detected. Standard handling is sufficient."
