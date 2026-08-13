import requests

from app.core.config import PHISHTANK_API_KEY

API_URL = "http://checkurl.phishtank.com/checkurl/"


def check_phishtank(url: str):

    headers = {
        "User-Agent": "EscudoFlowAI/1.0"
    }

    data = {
        "url": url,
        "format": "json"
    }

    if PHISHTANK_API_KEY:
        data["app_key"] = PHISHTANK_API_KEY

    try:

        response = requests.post(
            API_URL,
            headers=headers,
            data=data,
            timeout=15
        )

        response.raise_for_status()

        result = response.json()["results"]

        malicious = (
            result["in_database"] and
            result["verified"] == "y" and
            result["valid"] == "y"
        )

        return {

            "provider": "PhishTank",

            "status": "Malicious" if malicious else "Clean",

            "malicious": malicious,

            "phish_id": result.get("phish_id"),

            "verified": result.get("verified"),

            "valid": result.get("valid"),

            "detail_url": result.get("phish_detail_page")

        }

    except Exception as e:

        print(f"[PHISHTANK ERROR] {e}")

        return {

            "provider": "PhishTank",

            "status": "Unavailable",

            "malicious": False

        }