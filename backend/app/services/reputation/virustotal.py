import requests

from app.core.config import VIRUSTOTAL_API_KEY


API_URL = "https://www.virustotal.com/api/v3/urls"


def check_virustotal(url: str):
    """
    Check a URL using VirusTotal.
    """

    if not VIRUSTOTAL_API_KEY:
        return {
            "provider": "VirusTotal",
            "status": "API Key Missing",
            "malicious": False,
            "detections": "N/A"
        }

    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY
    }

    try:
        # Step 1: Submit URL
        submit = requests.post(
            API_URL,
            headers=headers,
            data={"url": url},
            timeout=15
        )

        submit.raise_for_status()

        analysis_id = submit.json()["data"]["id"]

        # Step 2: Get analysis
        analysis = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers,
            timeout=15
        )

        analysis.raise_for_status()

        stats = analysis.json()["data"]["attributes"]["stats"]

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless = stats.get("harmless", 0)

        return {
            "provider": "VirusTotal",
            "status": "Malicious" if malicious > 0 else "Clean",
            "malicious": malicious > 0,
            "detections": f"{malicious}/{malicious + suspicious + harmless}",
            "stats": stats
        }

    except Exception as e:

        print(f"[VIRUSTOTAL ERROR] {e}")

        return {
            "provider": "VirusTotal",
            "status": "Unavailable",
            "malicious": False,
            "detections": "N/A"
        }