from datetime import datetime, timezone
import whois


def get_whois_info(domain: str):
    """
    Fetch WHOIS information for a domain.
    """

    try:
        w = whois.whois(domain)

       

        # -------------------------
        # Creation Date
        # -------------------------

        creation_date = w.creation_date

        # -------------------------
        # Creation Date
        # -------------------------

        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            # Normalize to naive UTC if the registry returned a
            # timezone-aware datetime, so the subtraction below never fails.
            if creation_date.tzinfo is not None:
                creation_date = creation_date.astimezone(timezone.utc).replace(tzinfo=None)

            created_at = creation_date.strftime("%Y-%m-%d")
            domain_age = (datetime.now() - creation_date).days
            domain_age = f"{domain_age} days"
        else:
            created_at = "Unknown"
            domain_age = "Unknown"

        # -------------------------
        # Registrar
        # -------------------------

        registrar = w.registrar or "Unknown"

        # -------------------------
        # Country
        # -------------------------

        country = w.country or "Unknown"

        return {
            "domainAge": domain_age,
            "registrar": registrar,
            "country": country,
            "createdAt": created_at
        }

    except Exception as e:
        print(f"[WHOIS ERROR] {e}")

        return {
            "domainAge": "Unknown",
            "registrar": "Unknown",
            "country": "Unknown",
            "createdAt": "Unknown"
        }