import re
from urllib.parse import urlparse

from app.models.response_models import URLResponse


SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "update",
    "bank",
    "account",
    "password",
    "paypal",
    "signin"
]

SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd"
]


def analyze_url(url: str) -> URLResponse:

    reasons = []
    risk_score = 0

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    protocol = parsed.scheme
    https = protocol == "https"
    url_length = len(url)

    # 1. Suspicious keywords
    for word in SUSPICIOUS_KEYWORDS:
        if word in url.lower():
            reasons.append(f"Contains suspicious keyword: {word}")
            risk_score += 20

    # 2. Too many hyphens
    if domain.count("-") >= 2:
        reasons.append("Domain contains multiple hyphens")
        risk_score += 20

    # 3. IP address instead of domain
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", domain):
        reasons.append("Uses IP address instead of domain name")
        risk_score += 30

    # 4. URL shortener
    if domain in SHORTENERS:
        reasons.append("Uses URL shortening service")
        risk_score += 20

    # Final prediction
    if risk_score >= 40:
        prediction = "Phishing"
        confidence = 0.95
    else:
        prediction = "Safe"
        confidence = 0.98
    

    return URLResponse(
        url=url,
        domain=domain,
        protocol=protocol,
        url_length=url_length,
        https=https,
        prediction=prediction,
        confidence=confidence,
        risk_score=risk_score,
        reasons=reasons,
    )