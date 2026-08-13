import requests

from app.core.config import GOOGLE_SAFE_BROWSING_API_KEY


API_URL = (
    "https://safebrowsing.googleapis.com/v4/threatMatches:find"
)


def check_google_safe_browsing(url: str):
    """
    Check a URL using Google Safe Browsing.
    """

    if not GOOGLE_SAFE_BROWSING_API_KEY:

        return {
            "provider": "Google Safe Browsing",
            "status": "API Key Missing",
            "malicious": False,
            "threats": []
        }

    payload = {
        "client": {
            "clientId": "EscudoFlowAI",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": [
                "ANY_PLATFORM"
            ],
            "threatEntryTypes": [
                "URL"
            ],
            "threatEntries": [
                {
                    "url": url
                }
            ]
        }
    }

    try:

        response = requests.post(
            f"{API_URL}?key={GOOGLE_SAFE_BROWSING_API_KEY}",
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        if "matches" not in result:

            return {
                "provider": "Google Safe Browsing",
                "status": "Clean",
                "malicious": False,
                "threats": []
            }

        threats = []

        for match in result["matches"]:

            threats.append(
                match["threatType"]
            )

        return {

            "provider": "Google Safe Browsing",

            "status": "Malicious",

            "malicious": True,

            "threats": threats

        }

    except Exception as e:

        print(f"[GOOGLE SAFE BROWSING ERROR] {e}")

        return {

            "provider": "Google Safe Browsing",

            "status": "Unavailable",

            "malicious": False,

            "threats": []

        }