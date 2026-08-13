import re
from urllib.parse import urlparse


URL_PATTERN = re.compile(
    r"(https?://[^\s]+|www\.[^\s]+|[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
    re.IGNORECASE,
)


def extract_url(ocr_result, user_url=None):
    """
    Extract a URL from either:
    1. User supplied URL
    2. OCR text inside screenshot
    """

    # User supplied URL takes priority
    if user_url:

        url = user_url.strip()

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        return {
            "url": url,
            "source": "user"
        }

    text = " ".join(
        ocr_result.get("text", [])
    )

    match = URL_PATTERN.search(text)

    if not match:
        return {
            "url": "",
            "source": "none"
        }

    url = match.group(0)

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return {
        "url": url,
        "source": "ocr"
    }


def extract_domain(url):

    if not url:
        return ""

    parsed = urlparse(url)

    return parsed.netloc.lower().replace("www.", "")