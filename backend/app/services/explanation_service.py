def generate_email_explanation(

    rule_result,

    auth_result,

    reply_result,

    entities,

    fusion

):

    reasons = []

    recommendations = []

    # -------------------------
    # Rule Engine Reasons
    # -------------------------

    reasons.extend(rule_result["reasons"])

    if auth_result["spf"] != "PASS":
        reasons.append("SPF validation failed.")

    if auth_result["dkim"] != "PASS":
        reasons.append("DKIM validation failed.")

    if auth_result["dmarc"] != "PASS":
        reasons.append("DMARC validation failed.")

    if not reply_result["match"]:
        reasons.append(reply_result["reason"])

    if entities["amount"]:
        reasons.append("Financial amount detected.")

    if entities["deadline"]:
        reasons.append("Urgent language detected.")

    # -------------------------
    # Recommendations
    # -------------------------

    recommendations = [

        "Do not click any links before verifying the sender.",

        "Verify the sender through another communication channel.",

        "Do not transfer money without independent confirmation.",

        "Report this email to your security team if it appears suspicious.",

        "Check the sender domain carefully before replying."

    ]

    # -------------------------
    # Summary
    # -------------------------

    summary = (

        f"This email has been classified as "

        f"{fusion['verdict']} risk "

        f"with an overall risk score of "

        f"{fusion['risk_score']}%. "

        f"The analysis identified multiple phishing indicators "

        f"including authentication issues, suspicious language "

        f"and sender verification concerns."

    )

    return {

        "summary": summary,

        "reasons": reasons,

        "recommendations": recommendations

    }