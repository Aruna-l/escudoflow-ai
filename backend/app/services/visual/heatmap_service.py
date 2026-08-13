import cv2
from pathlib import Path


RESULT_DIR = Path("uploads/visual/results")
RESULT_DIR.mkdir(parents=True, exist_ok=True)


def generate_heatmap(

    image_path,

    ocr_result,

    logo_result,

    qr_result,

    form_result

):
    """
    Draw AI detections on the screenshot.
    """

    image = cv2.imread(image_path)

    if image is None:
        return ""

    # ----------------------------
    # OCR
    # ----------------------------

    for detection in ocr_result.get("detections", []):

        box = detection.get("box")

        if not box:
            continue

        x1 = int(box[0][0])
        y1 = int(box[0][1])

        x2 = int(box[2][0])
        y2 = int(box[2][1])

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2
        )

        cv2.putText(
            image,
            "OCR",
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            2
        )

    # ----------------------------
    # Logo
    # ----------------------------

    if logo_result["detected"]:

        cv2.putText(

            image,

            f"Logo: {logo_result['brand']}",

            (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0, 255, 0),

            2

        )

    # ----------------------------
    # Login Form
    # ----------------------------

    if form_result["loginForm"]:

        cv2.putText(

            image,

            "Credential Collection Page",

            (20, 80),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0, 0, 255),

            2

        )

    # ----------------------------
    # QR
    # ----------------------------

    if qr_result["found"]:

        cv2.putText(

            image,

            "QR Detected",

            (20, 120),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (255, 0, 255),

            2

        )

    output = RESULT_DIR / "heatmap.png"

    cv2.imwrite(
        str(output),
        image
    )

    return str(output)