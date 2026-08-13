def detect_clone(
    brand_result,
    similarity,
    domain_result,
    form_result
):
    """
    Detect whether the uploaded screenshot
    is likely a cloned phishing page.
    """

    score = 0

    reasons = []

    # ----------------------------
    # Brand detected
    # ----------------------------

    if brand_result["brand"] != "Unknown":
        score += 20
        reasons.append(
            f"{brand_result['brand']} brand detected"
        )

    # ----------------------------
    # Visual similarity
    # ----------------------------

    visual = similarity["visualSimilarity"]

    if visual >= 0.90:
        score += 40
        reasons.append(
            "Very high visual similarity"
        )

    elif visual >= 0.75:
        score += 30
        reasons.append(
            "High visual similarity"
        )

    elif visual >= 0.60:
        score += 15

    # ----------------------------
    # Login page
    # ----------------------------

    if form_result["loginForm"]:
        score += 20
        reasons.append(
            "Credential collection page"
        )

    # ----------------------------
    # Domain mismatch
    # ----------------------------

    if not domain_result["match"]:
        score += 20
        reasons.append(
            "Brand and domain mismatch"
        )

    score = min(score, 100)

    return {

        "isClone": score >= 70,

        "cloneProbability": score,

        "matchedBrand": brand_result["brand"],

        "referenceMatched": similarity.get(
            "referenceMatched",
            "Unknown"
        ),

        "reasons": reasons

    }