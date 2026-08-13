import os
import easyocr

from app.services.visual.preprocessing_service import preprocess_image


# Load EasyOCR only once
reader = easyocr.Reader(
    ["en"],
    gpu=False
)


def extract_text(image_path: str):
    """
    Extract text from an image after preprocessing.
    """

    processed = preprocess_image(image_path)

    result = reader.readtext(
        processed,
        paragraph=True,
        detail=1,
        contrast_ths=0.05,
        adjust_contrast=0.8,
        text_threshold=0.4,
        low_text=0.2
    )

    extracted_text = []

    detections = []

    total_confidence = 0.0

    for detection in result:
        if len(detection) == 3:
            bbox, text, confidence = detection
        else:
            bbox, text = detection
            confidence = 0.0

        clean_bbox = [
            [int(x), int(y)]
            for x, y in bbox
        ]

        extracted_text.append(text)

        total_confidence += confidence

        detections.append({

            "text": text,

            "confidence": round(float(confidence), 3),

            "bbox": clean_bbox

        })

    # -----------------------------
    # Average Confidence
    # -----------------------------

    if len(result) > 0:

        average_confidence = round(

            (total_confidence / len(result)) * 100,

            2

        )

    else:

        average_confidence = 0

    # -----------------------------
    # Delete temporary processed image
    # -----------------------------

    if processed != image_path and os.path.exists(processed):

        os.remove(processed)

    # -----------------------------
    # Final Response
    # -----------------------------

    return {

        "text": " ".join(extracted_text),

        "words": extracted_text,

        "detections": detections,

        "confidence": average_confidence,

        "language": "en"

    }