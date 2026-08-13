import socket
import ssl
from datetime import datetime


def get_ssl_info(domain: str):
    """
    Fetch SSL certificate information for a domain.
    """

    try:
        context = ssl.create_default_context()

        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:

                cert = ssock.getpeercert()

        issuer = dict(x[0] for x in cert["issuer"])

        issuer_name = issuer.get("organizationName") or issuer.get("commonName", "Unknown")

        valid_from = datetime.strptime(
            cert["notBefore"],
            "%b %d %H:%M:%S %Y %Z"
        )

        valid_to = datetime.strptime(
            cert["notAfter"],
            "%b %d %H:%M:%S %Y %Z"
        )

        now = datetime.utcnow()

        is_valid = valid_from <= now <= valid_to

        return {
            "issuer": issuer_name,
            "valid": is_valid,
            "validFrom": valid_from.strftime("%Y-%m-%d"),
            "validTo": valid_to.strftime("%Y-%m-%d")
        }

    except Exception as e:

        print(f"[SSL ERROR] {e}")

        return {
            "issuer": "Unknown",
            "valid": False,
            "validFrom": "Unknown",
            "validTo": "Unknown"
        }