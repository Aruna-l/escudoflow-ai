def calculate_metrics(
    similarity_result,
    logo_result,
    qr_result,
    brand_result
):
    """
    Aggregate all visual metrics into a single
    frontend-friendly structure.
    """

    return {

        # -----------------------------
        # Similarity Metrics
        # -----------------------------

        "visualSimilarity": float(similarity_result["visualSimilarity"]),

        "ssim": float(similarity_result["ssim"]),

        "clipSimilarity": float(similarity_result["clipSimilarity"]),

        "colorSimilarity": float(similarity_result["colorSimilarity"]),

        "layoutSimilarity": float(similarity_result["layoutSimilarity"]),

        "perceptualHash": int(similarity_result["perceptualHash"]),

        # -----------------------------
        # Logo
        # -----------------------------

        "logoDetected": bool(logo_result["detected"]),

        "logoConfidence": float(logo_result["confidence"]),

        "brand": logo_result["brand"],

        # -----------------------------
        # QR
        # -----------------------------

        "qrDetected": bool(qr_result["found"]),

        "qrCount": int(qr_result["count"]),

        # -----------------------------
        # Brand Similarity
        # -----------------------------

        "brandSimilarity": float(brand_result["brandSimilarity"])

    }