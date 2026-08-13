def calculate_visual_risk(

    logo_result,

    qr_result,

    brand_result,

    similarity_result,

    metrics

):
    """
    Calculate the overall visual phishing risk.
    """

    score = 0

    reasons = []

    # -----------------------------
    # Logo Detection
    # -----------------------------

    if logo_result["detected"]:

        score += 20

        reasons.append(

            f"{logo_result['brand']} logo detected."

        )

    # -----------------------------
    # QR Detection
    # -----------------------------

    if qr_result["found"]:

        score += 20

        reasons.append(

            f"{qr_result['count']} QR code(s) detected."

        )

    # -----------------------------
    # Brand Similarity
    # -----------------------------

    if brand_result["brandSimilarity"] >= 0.90:

        score += 25

        reasons.append(

            "Very high brand similarity."

        )

    elif brand_result["brandSimilarity"] >= 0.70:

        score += 15

        reasons.append(

            "Moderate brand similarity."

        )

    # -----------------------------
    # Visual Similarity
    # -----------------------------

    if metrics["visualSimilarity"] >= 0.90:

        score += 25

        reasons.append(

            "Screenshot closely matches an official page."

        )

    elif metrics["visualSimilarity"] >= 0.75:

        score += 15

        reasons.append(

            "Screenshot resembles an official page."

        )

    # -----------------------------
    # Final Score
    # -----------------------------

    score = min(score, 100)

    if score >= 80:

        verdict = "Critical"

    elif score >= 60:

        verdict = "High"

    elif score >= 40:

        verdict = "Medium"

    else:

        verdict = "Low"

    return {

        "riskScore": score,

        "confidence": min(score + 10, 100),

        "verdict": verdict,

        "reasons": reasons

    }