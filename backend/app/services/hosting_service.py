import socket
from ipwhois import IPWhois


def get_hosting_info(domain: str):
    """
    Fetch IP, Hosting Provider, ASN, Country and Reverse DNS.
    """

    try:

        # Resolve domain to IP
        ip = socket.gethostbyname(domain)

        # Reverse DNS
        try:
            reverse_dns = socket.gethostbyaddr(ip)[0]
        except Exception:
            reverse_dns = "Unknown"

        # WHOIS lookup for IP
        obj = IPWhois(ip)
        result = obj.lookup_rdap(depth=1)

        return {

            "ip": ip,

            "hosting": result.get("network", {}).get("name", "Unknown"),

            "asn": result.get("asn", "Unknown"),

            "country": result.get("asn_country_code", "Unknown"),

            "reverseDNS": reverse_dns

        }

    except Exception as e:

        print(f"[HOSTING ERROR] {e}")

        return {

            "ip": "Unknown",

            "hosting": "Unknown",

            "asn": "Unknown",

            "country": "Unknown",

            "reverseDNS": "Unknown"

        }