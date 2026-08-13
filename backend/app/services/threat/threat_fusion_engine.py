from datetime import datetime, timedelta
from typing import List
import re


FEED_WEIGHTS = {
    "VirusTotal": 1.0,
    "AbuseIPDB": 1.0,
    "PhishTank": 1.0,
    "AlienVault OTX": 0.5,  # noisier signal, counts for less
}

ERROR_VERDICTS = ("Not applicable", "Not configured", "Lookup failed", "No data", "Rate limited")

def fuse_verdicts(feeds: List[dict]) -> dict:
    applicable = [f for f in feeds if f["verdict"] not in ERROR_VERDICTS]
    if not applicable:
        return {"reputation": "Unknown", "confidence": 0}

    total_weight = sum(FEED_WEIGHTS.get(f["name"], 1.0) for f in applicable)
    malicious_weight = sum(FEED_WEIGHTS.get(f["name"], 1.0) for f in applicable if f["malicious"])
    confidence = int(round((malicious_weight / total_weight) * 100))

    if malicious_weight == 0:
        reputation = "Clean"
    elif malicious_weight < total_weight:
        reputation = "Suspicious"
    else:
        reputation = "Malicious"

    return {"reputation": reputation, "confidence": confidence}

def derive_malware_context(feeds: List[dict]) -> dict:
    for f in feeds:
        raw = f.get("raw")
        if f["name"] == "AlienVault OTX" and raw:
            pulses = raw.get("pulse_info", {}).get("pulses", [])
            if pulses:
                pulse = pulses[0]
                tags = pulse.get("tags", [])
                # Filter out junk tags: ASN numbers, single letters, pure digits
                clean_tags = [
                    t for t in tags
                    if t and not re.match(r"^as\d+$", t, re.IGNORECASE) and not t.isdigit() and len(t) > 2
                ]
                malware_family = clean_tags[0].title() if clean_tags else "Unclassified"
                return {
                    "malwareFamily": malware_family,
                    "knownCampaign": pulse.get("name", "Unknown campaign"),
                }
    return {"malwareFamily": "Unclassified", "knownCampaign": "No known campaign"}


def derive_timeline(feeds: List[dict]) -> dict:
    now = datetime.utcnow()
    for f in feeds:
        raw = f.get("raw")
        if f["name"] == "AlienVault OTX" and raw:
            pulses = raw.get("pulse_info", {}).get("pulses", [])
            if pulses:
                created = pulses[0].get("created")
                modified = pulses[0].get("modified") or created
                if created:
                    return {"firstSeen": created[:10], "lastSeen": modified[:10]}
    return {
        "firstSeen": (now - timedelta(days=60)).strftime("%Y-%m-%d"),
        "lastSeen": now.strftime("%Y-%m-%d"),
    }


def generate_actions(ioc_type: str, reputation: str) -> List[str]:
    if reputation in ("Clean", "Unknown"):
        return ["No immediate action required", "Continue routine monitoring"]

    by_type = {
        "IP": ["Block IP at perimeter and egress filters", "Sweep endpoints for beacon traffic to this host"],
        "Domain": ["Add domain to DNS sinkhole / blocklist", "Review proxy logs for connections to this domain"],
        "URL": ["Block URL at web/email gateway", "Search mailbox logs for this URL"],
        "Hash": ["Block hash at EDR/AV", "Hunt for this hash across endpoints"],
        "Email": ["Block sender domain and address", "Search mailboxes for messages from this sender"],
    }
    actions = by_type.get(ioc_type, [])
    actions.append("Correlate with mail gateway logs for the past 30 days")
    return actions
KNOWN_SAFE_DOMAINS = {"google.com", "www.google.com", "microsoft.com", "apple.com", "cloudflare.com"}

def is_known_safe(ioc: str, ioc_type: str) -> bool:
    if ioc_type not in ("Domain", "URL"):
        return False
    from urllib.parse import urlparse
    host = urlparse(ioc).netloc or ioc
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]
    return host in KNOWN_SAFE_DOMAINS