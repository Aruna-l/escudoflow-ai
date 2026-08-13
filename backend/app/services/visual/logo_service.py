import cv2
import os
from app.services.visual.orb_logo_service import detect_logo_orb


LOGO_DIR = "vision/logos"


def detect_logo(image_path: str):

    orb_result = detect_logo_orb(image_path)
    
    if orb_result["detected"]:
        return orb_result

    screenshot = cv2.imread(image_path)

    if screenshot is None:
        return {
            "detected": False,
            "brand": None,
            "confidence": 0
        }

    screenshot_gray = cv2.cvtColor(
        screenshot,
        cv2.COLOR_BGR2GRAY
    )

    screenshot_h, screenshot_w = screenshot_gray.shape[:2]

    best_brand = None
    best_score = 0

    for file in os.listdir(LOGO_DIR):

        if not file.endswith(".png"):
            continue

        logo_path = os.path.join(
            LOGO_DIR,
            file
        )

        logo = cv2.imread(
            logo_path,
            0
        )

        if logo is None:
            continue

        logo_h, logo_w = logo.shape[:2]

        # matchTemplate requires the template to be no larger than the
        # image in either dimension — skip logos that don't fit, and
        # downscale the logo if needed instead of crashing.
        if logo_h > screenshot_h or logo_w > screenshot_w:
            scale = min(
                screenshot_h / logo_h,
                screenshot_w / logo_w
            )
            new_w = max(1, int(logo_w * scale))
            new_h = max(1, int(logo_h * scale))
            logo = cv2.resize(logo, (new_w, new_h))

        result = cv2.matchTemplate(
            screenshot_gray,
            logo,
            cv2.TM_CCOEFF_NORMED
        )

        _, score, _, _ = cv2.minMaxLoc(result)

        if score > best_score:
            best_score = score
            best_brand = file.replace(".png", "")

    return {

        "detected": bool(best_score > 0.55),

        "brand": best_brand,

        "confidence": round(
            float(best_score) * 100,
            2
        )
    }
    