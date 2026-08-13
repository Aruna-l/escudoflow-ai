from app.services.url_service import analyze_url


def analyze_email_urls(urls):
    """
    Analyze every URL found inside an email.
    """

    results = []

    for url in urls:

        try:

            result = analyze_url(url)

            results.append({

                "url": url,

                "risk_score": result.risk_score,

                "prediction": result.prediction,

                "confidence": result.confidence

            })

        except Exception:

            results.append({

                "url": url,

                "risk_score": 0,

                "prediction": "Unknown",

                "confidence": 0

            })

    return results