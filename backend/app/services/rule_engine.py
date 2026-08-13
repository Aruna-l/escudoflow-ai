import re
from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "update",
    "bank",
    "account",
    "password",
    "paypal",
    "signin",
    "wallet",
    "confirm",
    "recover",
    "invoice"
]

SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "ow.ly",
    "buff.ly"
]


def analyze_rules(url: str):

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    score = 0

    reasons = []

    # -------------------------
    # Suspicious keywords
    # -------------------------

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in url.lower():

            score += 15

            reasons.append(
                f"Contains suspicious keyword: {keyword}"
            )

    # -------------------------
    # Too many hyphens
    # -------------------------

    hyphens = domain.count("-")

    if hyphens >= 2:

        score += 20

        reasons.append("Domain contains multiple hyphens")

    # -------------------------
    # Uses IP address
    # -------------------------

    if re.match(r"^\d+\.\d+\.\d+\.\d+$", domain):

        score += 30

        reasons.append("Uses IP address instead of domain")

    # -------------------------
    # URL shortener
    # -------------------------

    if domain in SHORTENERS:

        score += 20

        reasons.append("Uses URL shortening service")

    # -------------------------
    # Very long URL
    # -------------------------

    if len(url) > 75:

        score += 15

        reasons.append("Very long URL")

    # -------------------------
    # Too many digits
    # -------------------------

    digits = sum(c.isdigit() for c in url)

    if digits >= 8:

        score += 10

        reasons.append("Large number of digits")

    # -------------------------
    # Many special characters
    # -------------------------

    special = sum(
        not c.isalnum()
        for c in url
    )

    if special >= 15:

        score += 10

        reasons.append("Many special characters")

    # -------------------------
    # Cap score
    # -------------------------

    score = min(score, 100)

    return {

        "rule_score": score,

        "reasons": reasons

    }