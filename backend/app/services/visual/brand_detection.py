import re


# ---------------------------------
# Known Brand Keywords
# ---------------------------------

BRAND_KEYWORDS = {

    "Microsoft": [
        "microsoft",
        "office",
        "outlook",
        "onedrive",
        "azure",
        "office365",
        "m365"
    ],

    "Google": [
        "google",
        "gmail",
        "drive",
        "docs",
        "workspace",
        "accounts.google"
    ],

    "Apple": [
        "apple",
        "icloud",
        "apple id",
        "app store"
    ],

    "Amazon": [
        "amazon",
        "aws",
        "prime",
        "amazon pay"
    ],

    "PayPal": [
        "paypal",
        "paypal account",
        "paypal login"
    ],

    "GitHub": [
        "github",
        "repository",
        "pull request",
        "commit"
    ],

    "Adobe": [
        "adobe",
        "creative cloud",
        "acrobat",
        "photoshop"
    ],

    "LinkedIn": [
        "linkedin",
        "jobs",
        "network",
        "profile"
    ]

}


# ---------------------------------
# Detect Brand
# ---------------------------------

def detect_brand(ocr_result, logo_result):
    """
    Detect the most likely brand using OCR text
    and (later) logo detection.
    """

    detected_brand = "Unknown"

    confidence = 0

    text = " ".join(
        ocr_result.get("text", [])
    ).lower()

    # -------------------------
    # OCR Keyword Matching
    # -------------------------

    for brand, keywords in BRAND_KEYWORDS.items():

        matches = 0

        for keyword in keywords:

            if re.search(
                re.escape(keyword),
                text
            ):
                matches += 1

        if matches > confidence:

            confidence = matches

            detected_brand = brand

    # -------------------------
    # Logo Boost
    # -------------------------

    if logo_result.get("detected"):

        logo_brand = logo_result.get("brand")

        if logo_brand:

            detected_brand = logo_brand

            confidence += 2

    return {

        "brand": detected_brand,

        "confidence": confidence

    }