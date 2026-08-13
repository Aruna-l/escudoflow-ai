def generate_ai_explanation(
    url: str,
    final_result: dict,
    reputation: dict,
    brand_similarity: dict,
    https: bool,
):
    """
    Generates a human-readable AI explanation for the final verdict.
    """

    reasons = []
    recommendations = []

    # -----------------------------
    # Safe URL
    # -----------------------------

    if final_result["prediction"] == "Legitimate":

        summary = (
            "This URL appears to be legitimate. "
            "No significant phishing indicators were detected."
        )

        if https:
            reasons.append("Uses a secure HTTPS connection.")

        if reputation["summary"]["verdict"] == "Clean":
            reasons.append("Threat intelligence providers reported no malicious activity.")

        if final_result["rule_score"] == 0:
            reasons.append("Rule engine detected no suspicious URL patterns.")

        recommendations.extend([
            "Continue using normal browsing practices.",
            "Always verify sensitive websites before entering credentials."
        ])

    # -----------------------------
    # Suspicious URL
    # -----------------------------

    elif final_result["prediction"] == "Suspicious":

        summary = (
            "This URL exhibits suspicious characteristics. "
            "Although not confirmed as phishing, caution is recommended."
        )

        if not https:
            reasons.append("Website does not use HTTPS.")

        if final_result["rule_score"] > 0:
            reasons.append("Rule engine detected suspicious URL patterns.")

        if brand_similarity.get("isImpersonating"):
            reasons.append(
                f"Domain resembles '{brand_similarity.get('matchedBrand')}'."
            )

        recommendations.extend([
            "Avoid entering passwords.",
            "Verify the website before continuing.",
            "Use additional verification methods."
        ])

    # -----------------------------
    # Phishing
    # -----------------------------

    else:

        summary = (
            "This URL is highly likely to be a phishing website."
        )

        if reputation["summary"]["detections"] > 0:
            reasons.append(
                "Threat intelligence providers flagged this URL."
            )

        if brand_similarity.get("isImpersonating"):
            reasons.append(
                f"Impersonates '{brand_similarity.get('matchedBrand')}'."
            )

        if final_result["rule_score"] > 0:
            reasons.append("Multiple phishing indicators detected.")

        recommendations.extend([
            "Do NOT visit this website.",
            "Do NOT enter personal information.",
            "Block this domain immediately.",
            "Report the website to your security team."
        ])

    return {
        "summary": summary,
        "reasons": reasons,
        "recommendations": recommendations
    }