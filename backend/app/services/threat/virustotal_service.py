import base64
import httpx
from app.core import config
import logging

VT_BASE = "https://www.virustotal.com/api/v3"
logger = logging.getLogger("virustotal_service")


async def query_virustotal(ioc: str, ioc_type: str) -> dict:
    if not config.VIRUSTOTAL_API_KEY:
        return {"name": "VirusTotal", "verdict": "Not configured", "malicious": False, "raw": None}

    headers = {"x-apikey": config.VIRUSTOTAL_API_KEY}

    if ioc_type == "IP":
        url = f"{VT_BASE}/ip_addresses/{ioc}"
    elif ioc_type == "Domain":
        url = f"{VT_BASE}/domains/{ioc}"
    elif ioc_type == "URL":
        url_id = base64.urlsafe_b64encode(ioc.encode()).decode().strip("=")
        url = f"{VT_BASE}/urls/{url_id}"
    elif ioc_type == "Hash":
        url = f"{VT_BASE}/files/{ioc}"
    else:
        return {"name": "VirusTotal", "verdict": "Not applicable", "malicious": False, "raw": None}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code != 200:
                logger.warning(f"VirusTotal returned {resp.status_code}: {resp.text[:200]}")
                verdict = "Rate limited" if resp.status_code == 429 else "No data"
                return {"name": "VirusTotal", "verdict": verdict, "malicious": False, "raw": None}

            stats = resp.json()["data"]["attributes"]["last_analysis_stats"]
            malicious = stats.get("malicious", 0)
            total = sum(stats.values()) or 1
            return {
                "name": "VirusTotal",
                "verdict": f"{malicious} / {total} vendors",
                "malicious": malicious > 0,
                "raw": stats,
            }
    except Exception as e:
        logger.error(f"VirusTotal request failed: {e}")
        return {"name": "VirusTotal", "verdict": "Lookup failed", "malicious": False, "raw": None}