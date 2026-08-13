import socket
import requests

from app.core.config import ABUSEIPDB_API_KEY


API_URL = "https://api.abuseipdb.com/api/v2/check"


def check_abuseipdb(url: str):
    """
    Check IP reputation using AbuseIPDB.
    """

    if not ABUSEIPDB_API_KEY:
        return {
            "provider": "AbuseIPDB",
            "status": "API Key Missing",
            "malicious": False,
            "confidence": 0
        }

    try:

        # Get hostname
        hostname = url.split("//")[-1].split("/")[0]

        # Resolve IP
        ip = socket.gethostbyname(hostname)

        headers = {
            "Key": ABUSEIPDB_API_KEY,
            "Accept": "application/json"
        }

        params = {
            "ipAddress": ip,
            "maxAgeInDays": 90
        }

        response = requests.get(
            API_URL,
            headers=headers,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()["data"]

        confidence = data.get("abuseConfidenceScore", 0)

        return {

            "provider": "AbuseIPDB",

            "status": "Malicious" if confidence >= 50 else "Clean",

            "malicious": confidence >= 50,

            "confidence": confidence,

            "country": data.get("countryCode", "Unknown"),

            "isp": data.get("isp", "Unknown"),

            "usageType": data.get("usageType", "Unknown")

        }

    except Exception as e:

        print(f"[ABUSEIPDB ERROR] {e}")

        return {

            "provider": "AbuseIPDB",

            "status": "Unavailable",

            "malicious": False,

            "confidence": 0

        }