import httpx
from app.core import config

OTX_BASE = "https://otx.alienvault.com/api/v1/indicators"

SECTION_BY_TYPE = {"IP": "IPv4", "Domain": "domain", "URL": "url", "Hash": "file"}


async def query_alienvault(ioc: str, ioc_type: str) -> dict:
    section = SECTION_BY_TYPE.get(ioc_type)
    if not section:
        return {"name": "AlienVault OTX", "verdict": "Not applicable", "malicious": False, "raw": None}

    headers = {}
    if config.ALIENVAULT_OTX_API_KEY:
        headers["X-OTX-API-KEY"] = config.ALIENVAULT_OTX_API_KEY

    url = f"{OTX_BASE}/{section}/{ioc}/general"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code != 200:
                return {"name": "AlienVault OTX", "verdict": "No data", "malicious": False, "raw": None}
            data = resp.json()
            pulse_count = data.get("pulse_info", {}).get("count", 0)
            return {
                "name": "AlienVault OTX",
                "verdict": f"{pulse_count} pulses",
                "malicious": pulse_count >= 10,  # was: pulse_count > 0
                "raw": data,
            }
    except Exception:
        return {"name": "AlienVault OTX", "verdict": "Lookup failed", "malicious": False, "raw": None}