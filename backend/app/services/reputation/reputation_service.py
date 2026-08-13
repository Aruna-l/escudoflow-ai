from concurrent.futures import ThreadPoolExecutor

from app.services.reputation.google_safe_browsing import check_google_safe_browsing
from app.services.reputation.virustotal import check_virustotal
from app.services.reputation.abuseipdb import check_abuseipdb


def analyze_reputation(url: str):

    with ThreadPoolExecutor(max_workers=3) as executor:

        future_google = executor.submit(
            check_google_safe_browsing,
            url
        )

        future_virustotal = executor.submit(
            check_virustotal,
            url
        )

        future_abuseipdb = executor.submit(
            check_abuseipdb,
            url
        )

        providers = [
            future_google.result(),
            future_virustotal.result(),
            future_abuseipdb.result()
        ]

    detections = sum(
        1 for provider in providers
        if provider.get("malicious", False)
    )

    risk_score = int(
        (detections / len(providers)) * 100
    )

    if risk_score >= 70:
        verdict = "Malicious"
    elif risk_score >= 30:
        verdict = "Suspicious"
    else:
        verdict = "Clean"

    return {
        "providers": providers,
        "summary": {
            "detections": detections,
            "total_providers": len(providers),
            "risk_score": risk_score,
            "verdict": verdict
        }
    }