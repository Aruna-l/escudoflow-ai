from urllib.parse import urlparse


OFFICIAL_DOMAINS = {

    "Microsoft": [
        "microsoft.com",
        "office.com",
        "office365.com",
        "live.com",
        "outlook.com"
    ],

    "Google": [
        "google.com",
        "gmail.com",
        "googleusercontent.com"
    ],

    "GitHub": [
        "github.com"
    ],

    "PayPal": [
        "paypal.com"
    ],

    "Amazon": [
        "amazon.com",
        "amazon.in"
    ],

    "Apple": [
        "apple.com",
        "icloud.com"
    ],

    "Adobe": [
        "adobe.com"
    ],

    "LinkedIn": [
        "linkedin.com"
    ]
}


def match_domain(url, detected_brand):

    if not url:

        return {

            "domain": "",

            "expected": [],

            "match": False,

            "score": 0,

            "reason": "No URL available"

        }

    parsed = urlparse(url)

    domain = parsed.netloc.lower().replace("www.", "")

    expected = OFFICIAL_DOMAINS.get(
        detected_brand,
        []
    )

    matched = any(

        domain.endswith(x)

        for x in expected

    )

    score = 100 if matched else 0

    return {

        "domain": domain,

        "expected": expected,

        "match": matched,

        "score": score,

        "reason": (

            "Official domain"

            if matched

            else

            "Domain does not match detected brand"

        )

    }