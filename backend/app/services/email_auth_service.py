def analyze_email_auth(email_data):
    """
    Simulated SPF / DKIM / DMARC analysis.
    """

    sender = email_data["from"].lower()

    score = 0

    spf = "PASS"
    dkim = "PASS"
    dmarc = "PASS"

    # Demo logic

    if "gmail.com" in sender:
        spf = "PASS"
        dkim = "PASS"
        dmarc = "PASS"

    elif "protonmail" in sender:
        spf = "FAIL"
        dkim = "NONE"
        dmarc = "FAIL"
        score = 40

    else:
        spf = "PASS"
        dkim = "FAIL"
        dmarc = "FAIL"
        score = 20

    return {

        "spf": spf,

        "dkim": dkim,

        "dmarc": dmarc,

        "score": score

    }