def fuse_results(

    brand_result,

    similarity,

    domain_result,

    qr_result,

    form_result=None

):
    """
    Combine visual intelligence with
    domain intelligence.
    """

    score = 0

    reasons = []

    # -----------------------------
    # Brand detected
    # -----------------------------

    if brand_result["brand"] != "Unknown":

        score += 20

        reasons.append(

            f"{brand_result['brand']} detected"

        )

    # -----------------------------
    # Visual similarity
    # -----------------------------

    visual = similarity["visualSimilarity"]

    score += visual * 40

    if visual > 0.85:

        reasons.append(

            "Very high visual similarity"

        )

    elif visual > 0.65:

        reasons.append(

            "Moderate visual similarity"

        )

    # -----------------------------
    # Domain
    # -----------------------------

    if domain_result["match"]:

        score -= 20

        reasons.append(

            "Official domain"

        )

    else:

        score += 30

        reasons.append(

            "Domain mismatch"

        )

    # -----------------------------
    # QR
    # -----------------------------

    if qr_result["found"]:

        score += 10

        reasons.append(

            "QR code detected"

        )

    # -----------------------------
    # Login Form
    # -----------------------------

    if form_result:

        if form_result.get("loginForm"):

            score += 15

            reasons.append(

                "Credential collection page"

            )

    score = max(0, min(score, 100))

    if score >= 80:

        verdict = "Critical"

    elif score >= 60:

        verdict = "High"

    elif score >= 40:

        verdict = "Medium"

    else:

        verdict = "Low"

    return {

        "fusionRisk": round(score, 2),

        "verdict": verdict,

        "reasons": reasons,

        "domain": domain_result,

        "visualSimilarity": similarity["visualSimilarity"],

        "detectedBrand": brand_result["brand"]

    }