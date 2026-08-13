from urllib.parse import urlparse
import ipaddress
import re


def extract_features(url: str):
    """
    Extract URL-based features for the production ML model.
    """

    parsed = urlparse(url)
    domain = parsed.netloc

    features = {}

    # -------------------------
    # Basic Features
    # -------------------------

    features["URLLength"] = len(url)
    features["DomainLength"] = len(domain)

    features["IsHTTPS"] = 1 if parsed.scheme.lower() == "https" else 0

    # TLD
    if "." in domain:
        tld = domain.split(".")[-1]
    else:
        tld = ""

    features["TLD"] = tld
    features["TLDLength"] = len(tld)

    # Domain is IP?
    try:
        ipaddress.ip_address(domain)
        features["IsDomainIP"] = 1
    except ValueError:
        features["IsDomainIP"] = 0

    # -------------------------
    # Structural Features
    # -------------------------

    # Number of Subdomains
    if domain:
        features["NoOfSubDomain"] = max(domain.count(".") - 1, 0)
    else:
        features["NoOfSubDomain"] = 0

    # Letters
    letters = sum(c.isalpha() for c in url)
    features["NoOfLettersInURL"] = letters

    # Digits
    digits = sum(c.isdigit() for c in url)
    features["NoOfDegitsInURL"] = digits

    # Ratios
    total_length = len(url)

    features["LetterRatioInURL"] = (
        letters / total_length if total_length else 0
    )

    features["DegitRatioInURL"] = (
        digits / total_length if total_length else 0
    )

    # Obfuscation
    features["HasObfuscation"] = 1 if "%" in url else 0

    obfuscated_chars = url.count("%")

    features["NoOfObfuscatedChar"] = obfuscated_chars

    features["ObfuscationRatio"] = (
        obfuscated_chars / total_length if total_length else 0
    )

        # -------------------------
    # Special Character Features
    # -------------------------

    # Number of '='
    features["NoOfEqualsInURL"] = url.count("=")

    # Number of '?'
    features["NoOfQMarkInURL"] = url.count("?")

    # Number of '&'
    features["NoOfAmpersandInURL"] = url.count("&")

    # Other special characters
    special_chars = set("!@#$^*()_+-={}[]|\\:;\"'<>,./~`")

    other_special = sum(
        1 for ch in url
        if ch in special_chars and ch not in ["=", "?", "&"]
    )

    features["NoOfOtherSpecialCharsInURL"] = other_special

    # Ratio of all special characters
    total_length = len(url)

    total_special = sum(
        1 for ch in url
        if not ch.isalnum()
    )

    features["SpacialCharRatioInURL"] = (
        total_special / total_length
        if total_length else 0
    )

    return features


if __name__ == "__main__":

    url = ""

    result = extract_features(url)

    for key, value in result.items():
        print(f"{key}: {value}")