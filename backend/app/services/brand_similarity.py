from urllib.parse import urlparse
from rapidfuzz import fuzz

# Trusted brands
KNOWN_BRANDS = [
    "paypal",
    "google",
    "microsoft",
    "apple",
    "amazon",
    "facebook",
    "instagram",
    "netflix",
    "github",
    "linkedin",
    "dropbox",
    "adobe",
    "spotify",
    "twitter",
    "discord",
    "steam",
    "outlook",
    "office365",
    "bankofamerica",
    "icici",
    "hdfc",
    "sbi"
]


# Common homoglyph substitutions
HOMOGLYPHS = {
    "0": "o",
    "1": "l",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "@": "a",
    "$": "s",
    "!": "i"
}


def normalize(text: str) -> str:
    """
    Replace common phishing homoglyphs.
    """
    text = text.lower()

    for fake, real in HOMOGLYPHS.items():
        text = text.replace(fake, real)

    return text


def get_brand_similarity(url: str):

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    domain = domain.replace("www.", "")

    normalized = normalize(domain)

    best_brand = None
    best_score = 0

    for brand in KNOWN_BRANDS:

        score = fuzz.partial_ratio(
            normalized,
            brand
        )

        if score > best_score:
            best_score = score
            best_brand = brand

    reasons = []

    if best_score >= 80:
        reasons.append(
            f"Domain resembles '{best_brand}'"
        )

    if normalized != domain:
        reasons.append(
            "Possible homoglyph attack"
        )

    return {

        "brandSimilarity": best_score,

        "matchedBrand": best_brand if best_score >= 70 else "None",

        "isImpersonating": best_score >= 80,

        "reasons": reasons

    }