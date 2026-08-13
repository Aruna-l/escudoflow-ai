def calculate_brand_similarity(

    ocr_result,

    logo_result,

    similarity_result

):
    """
    Combine OCR, Logo Detection and Visual Similarity
    to estimate confidence that the screenshot belongs
    to a particular brand.
    """

    # ---------------------------------
    # OCR Text
    # ---------------------------------

    text = ocr_result.get(
        "text",
        ""
    ).lower()

    # ---------------------------------
    # Logo
    # ---------------------------------

    detected_brand = logo_result.get(
        "brand"
    )

    logo_confidence = logo_result.get(
        "confidence",
        0
    )

    # ---------------------------------
    # Visual Similarity
    # ---------------------------------

    visual_similarity = similarity_result.get(
        "visualSimilarity",
        0
    )

    # ---------------------------------
    # Score
    # ---------------------------------

    score = 0

    reasons = []

    if detected_brand:

        score += 40

        reasons.append(
            f"{detected_brand} logo detected."
        )

    if visual_similarity >= 0.90:

        score += 40

        reasons.append(
            "Very high visual similarity."
        )

    elif visual_similarity >= 0.75:

        score += 25

        reasons.append(
            "Moderate visual similarity."
        )

    if detected_brand:

        brand_lower = detected_brand.lower()

        if brand_lower in text:

            score += 20

            reasons.append(
                f"{detected_brand} found in OCR text."
            )

    score = min(score, 100)

    return {

        "matchedBrand": detected_brand
        if detected_brand
        else "Unknown",

        "brandSimilarity": round(
            score / 100,
            2
        ),

        "logoConfidence": logo_confidence,

        "reasons": reasons

    }