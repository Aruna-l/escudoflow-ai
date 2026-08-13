from app.services.visual.ocr_service import extract_text
from app.services.visual.logo_service import detect_logo
from app.services.visual.qr_service import detect_qr
from app.services.visual.brand_detection import detect_brand
from app.services.visual.visual_brand_similarity import calculate_brand_similarity
from app.services.visual.metrics_service import calculate_metrics
from app.services.visual.visual_risk_engine import calculate_visual_risk
from app.services.visual.visual_explanation import generate_visual_explanation
from app.services.visual.reference_service import get_reference_images
from app.services.visual.form_detector import detect_login_form
from app.services.visual.url_extractor import extract_url
from app.services.visual.domain_matcher import match_domain
from app.services.visual.fusion_service import fuse_results
from app.services.visual.clone_detector import detect_clone
from app.services.visual.similarity_service import (
    compare_brand,
    compare_against_references
)
from app.services.visual.heatmap_service import generate_heatmap



def analyze_visual(image_path, user_url=None):

    # --------------------------------
    # OCR
    # --------------------------------

    ocr_result = extract_text(image_path)
    form_result = detect_login_form(
        ocr_result
    )
    # --------------------------------
    # Logo Detection
    # --------------------------------

    logo_result = detect_logo(image_path)

    # --------------------------------
    # QR Detection
    # --------------------------------

    qr_result = detect_qr(image_path)

    # --------------------------------
    # Brand Detection
    # --------------------------------

    brand_result = detect_brand(
        ocr_result,
        logo_result
    )

    brand = brand_result["brand"]

    # --------------------------------
    # URL Extraction
    # --------------------------------

    url_result = extract_url(
        ocr_result,
        user_url
    )

    # --------------------------------
    # Domain Matching
    # --------------------------------

    domain_result = match_domain(
        url_result["url"],
        brand
    )

    # --------------------------------
    # Reference Image
    # --------------------------------

    reference_images = get_reference_images(
        brand
    )

    similarity = compare_against_references(
        image_path,
        reference_images
    )

    # --------------------------------
    # Fusion Engine
    # --------------------------------

    fusion = fuse_results(
        brand_result,
        similarity,
        domain_result,
        qr_result,
        form_result
    )
    clone_result = detect_clone(

        brand_result,

        similarity,

        domain_result,

        form_result

    )

    heatmap = generate_heatmap(

        image_path,

        ocr_result,

        logo_result,

        qr_result,

        form_result

    )
    # --------------------------------
    # Brand Similarity
    # --------------------------------

    brand_similarity = calculate_brand_similarity(
        ocr_result,
        logo_result,
        similarity
    )

    # --------------------------------
    # Metrics
    # --------------------------------

    metrics = calculate_metrics(
        similarity,
        logo_result,
        qr_result,
        brand_similarity
    )

    # --------------------------------
    # Risk Engine
    # --------------------------------

    risk = calculate_visual_risk(
        logo_result,
        qr_result,
        brand_similarity,
        similarity,
        metrics
    )

    # calculate_visual_risk returns "riskScore", not "overallRisk" —
    # read the correct key here.
    overall_risk = risk["riskScore"]
    confidence = risk["confidence"]
    verdict = risk["verdict"]

    # --------------------------------
    # AI Explanation
    # --------------------------------

    explanation = generate_visual_explanation(

        ocr_result,

        logo_result,

        qr_result,

        brand_similarity,

        metrics,

        risk,

        fusion,

        form_result,

        clone_result

    )

    # --------------------------------
    # Final Response
    # --------------------------------

    return {

        "ocr": ocr_result,

        "form": form_result,

        "clone": clone_result,

        "heatmap": heatmap,

        "logo": logo_result,

        "qr": qr_result,

        "brand": brand_similarity,

        "url": url_result,

        "domain": domain_result,

        "fusion": fusion,

        "similarity": similarity,

        "metrics": metrics,

        "overallRisk": overall_risk,

        "confidence": confidence,

        "verdict": verdict,

        "aiExplanation": explanation

    }