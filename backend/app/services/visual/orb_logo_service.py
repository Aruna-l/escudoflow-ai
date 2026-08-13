import cv2
import os

LOGO_DIR = "vision/logos"


def detect_logo_orb(image_path):
    """
    Detect logo using ORB feature matching.
    """

    uploaded = cv2.imread(image_path)

    if uploaded is None:
        return {
            "detected": False,
            "brand": None,
            "confidence": 0
        }

    gray_uploaded = cv2.cvtColor(
        uploaded,
        cv2.COLOR_BGR2GRAY
    )

    orb = cv2.ORB_create(1500)

    kp1, des1 = orb.detectAndCompute(
        gray_uploaded,
        None
    )

    if des1 is None:
        return {
            "detected": False,
            "brand": None,
            "confidence": 0
        }

    bf = cv2.BFMatcher(
        cv2.NORM_HAMMING,
        crossCheck=True
    )

    best_brand = None
    best_matches = 0

    for file in os.listdir(LOGO_DIR):

        path = os.path.join(
            LOGO_DIR,
            file
        )

        logo = cv2.imread(path)

        if logo is None:
            continue

        gray_logo = cv2.cvtColor(
            logo,
            cv2.COLOR_BGR2GRAY
        )

        kp2, des2 = orb.detectAndCompute(
            gray_logo,
            None
        )

        if des2 is None:
            continue

        matches = bf.match(
            des1,
            des2
        )

        matches = sorted(
            matches,
            key=lambda x: x.distance
        )

        good = [

            m for m in matches

            if m.distance < 60

        ]

        if len(good) > best_matches:

            best_matches = len(good)

            best_brand = os.path.splitext(file)[0]

    confidence = min(
        best_matches * 2,
        100
    )

    return {

        "detected": best_brand is not None,

        "brand": best_brand,

        "confidence": confidence

    }