import httpx
from app.core import config

AIPDB_URL = "https://api.abuseipdb.com/api/v2/check"


async def query_abuseipdb(ioc: str, ioc_type: str) -> dict:
    if ioc_type != "IP":
        return {"name": "AbuseIPDB", "verdict": "Not applicable", "malicious": False, "raw": None}
    if not config.ABUSEIPDB_API_KEY:
        return {"name": "AbuseIPDB", "verdict": "Not configured", "malicious": False, "raw": None}

    headers = {"Key": config.ABUSEIPDB_API_KEY, "Accept": "application/json"}
    params = {"ipAddress": ioc, "maxAgeInDays": 90}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(AIPDB_URL, headers=headers, params=params)
            if resp.status_code != 200:
                return {"name": "AbuseIPDB", "verdict": "No data", "malicious": False, "raw": None}
            data = resp.json()["data"]
            score = data.get("abuseConfidenceScore", 0)
            return {
                "name": "AbuseIPDB",
                "verdict": f"Confidence {score}%",
                "malicious": score >= 50,
                "raw": data,
            }
    except Exception:
        return {"name": "AbuseIPDB", "verdict": "Lookup failed", "malicious": False, "raw": None}