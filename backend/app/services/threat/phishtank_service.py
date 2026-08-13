import httpx
from app.core import config

PHISHTANK_URL = "https://checkurl.phishtank.com/checkurl/"


async def query_phishtank(ioc: str, ioc_type: str) -> dict:
    if ioc_type != "URL":
        return {"name": "PhishTank", "verdict": "Not applicable", "malicious": False, "raw": None}

    data = {"url": ioc, "format": "json"}
    if config.PHISHTANK_API_KEY:
        data["app_key"] = config.PHISHTANK_API_KEY

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(PHISHTANK_URL, data=data)
            if resp.status_code != 200:
                return {"name": "PhishTank", "verdict": "No data", "malicious": False, "raw": None}
            result = resp.json().get("results", {})
            in_db = result.get("in_database", False)
            verified = result.get("verified", False)
            if in_db and verified:
                verdict, malicious = "Reported (verified phish)", True
            elif in_db:
                verdict, malicious = "Reported (unverified)", True
            else:
                verdict, malicious = "Not reported", False
            return {"name": "PhishTank", "verdict": verdict, "malicious": malicious, "raw": result}
    except Exception:
        return {"name": "PhishTank", "verdict": "Lookup failed", "malicious": False, "raw": None}