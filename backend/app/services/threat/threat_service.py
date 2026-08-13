import asyncio
from app.services.threat.virustotal_service import query_virustotal
from app.services.threat.abuseipdb_service import query_abuseipdb
from app.services.threat.phishtank_service import query_phishtank
from app.services.threat.alienvault_service import query_alienvault
from app.services.threat.threat_fusion_engine import (
    fuse_verdicts,
    derive_malware_context,
    derive_timeline,
    generate_actions,
    is_known_safe,
)


async def analyze_ioc(ioc: str, ioc_type: str) -> dict:
    # Short-circuit well-known safe domains before hitting any feeds.
    # Avoids noisy OTX pulse-count false positives on major, benign infrastructure.
    if is_known_safe(ioc, ioc_type):
        return {
            "ioc": ioc,
            "type": ioc_type,
            "reputation": "Clean",
            "confidence": 0,
            "malwareFamily": "Unclassified",
            "knownCampaign": "No known campaign",
            "firstSeen": "N/A",
            "lastSeen": "N/A",
            "feeds": [
                {"name": "VirusTotal", "verdict": "Known safe domain", "malicious": False, "raw": None},
                {"name": "AbuseIPDB", "verdict": "Not applicable", "malicious": False, "raw": None},
                {"name": "PhishTank", "verdict": "Not applicable", "malicious": False, "raw": None},
                {"name": "AlienVault OTX", "verdict": "Known safe domain", "malicious": False, "raw": None},
            ],
            "actions": ["No immediate action required", "Continue routine monitoring"],
        }

    results = await asyncio.gather(
        query_virustotal(ioc, ioc_type),
        query_abuseipdb(ioc, ioc_type),
        query_phishtank(ioc, ioc_type),
        query_alienvault(ioc, ioc_type),
    )

    fusion = fuse_verdicts(results)
    context = derive_malware_context(results)
    timeline = derive_timeline(results)
    actions = generate_actions(ioc_type, fusion["reputation"])

    return {
        "ioc": ioc,
        "type": ioc_type,
        "reputation": fusion["reputation"],
        "confidence": fusion["confidence"],
        "malwareFamily": context["malwareFamily"],
        "knownCampaign": context["knownCampaign"],
        "firstSeen": timeline["firstSeen"],
        "lastSeen": timeline["lastSeen"],
        "feeds": results,
        "actions": actions,
    }