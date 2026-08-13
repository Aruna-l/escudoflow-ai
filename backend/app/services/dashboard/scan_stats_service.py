from datetime import datetime
from typing import List, Dict, Any

# Append-only log of every individual analyze call, regardless of verdict.
# Deliberately separate from _REPORTS, which only keeps the latest fused
# incident per session — a session with 5 scans still shows as 1 report
# there. This is the actual source for "total scans" / "safe messages".
_SCAN_LOG: List[Dict[str, Any]] = []


def record_scan(source_type: str, is_malicious: bool) -> None:
    _SCAN_LOG.append({
        "type": source_type,
        "is_malicious": is_malicious,
        "ts": datetime.utcnow(),
    })


def _scans_up_to(cutoff: datetime) -> List[Dict[str, Any]]:
    return [s for s in _SCAN_LOG if s["ts"] <= cutoff]


def total_scans_up_to(cutoff: datetime) -> int:
    return len(_scans_up_to(cutoff))


def safe_scans_up_to(cutoff: datetime) -> int:
    return len([s for s in _scans_up_to(cutoff) if not s["is_malicious"]])