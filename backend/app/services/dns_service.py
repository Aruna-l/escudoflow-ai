import dns.resolver
from urllib.parse import urlparse


def get_dns_info(url: str):
    """
    Fetch DNS records for a URL or domain.
    """

    # Extract domain if a full URL is passed
    if url.startswith(("http://", "https://")):
        domain = urlparse(url).netloc
    else:
        domain = url

    dns_info = {
        "a_records": [],
        "ns_records": [],
        "mx_records": []
    }

    # -------------------------
    # A Records
    # -------------------------

    try:
        answers = dns.resolver.resolve(domain, "A")

        dns_info["a_records"] = [
            answer.to_text()
            for answer in answers
        ]

    except Exception:
        pass

    # -------------------------
    # NS Records
    # -------------------------

    try:
        answers = dns.resolver.resolve(domain, "NS")

        dns_info["ns_records"] = [
            answer.to_text()
            for answer in answers
        ]

    except Exception:
        pass

    # -------------------------
    # MX Records
    # -------------------------

    try:
        answers = dns.resolver.resolve(domain, "MX")

        dns_info["mx_records"] = [
            answer.exchange.to_text()
            for answer in answers
        ]

    except Exception:
        pass

    return dns_info