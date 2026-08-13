import cv2


def detect_qr(image_path: str):

    image = cv2.imread(image_path)

    if image is None:
        return {
            "found": False,
            "count": 0,
            "data": []
        }

    detector = cv2.QRCodeDetector()

    success, decoded_info, points, _ = detector.detectAndDecodeMulti(image)

    if not success or points is None:

        return {
            "found": False,
            "count": 0,
            "data": []
        }

    qr_codes = []

    for text in decoded_info:

        qr_codes.append({
            "content": text if text else "",
            "suspicious": bool(text.startswith("http")) if text else False
        })

    return {
        "found": bool(success),
        "count": int(len(qr_codes)),
        "data": qr_codes
    }