import cv2


def calculate_color_similarity(image1_path, image2_path):
    """
    Compare two images using HSV color histogram similarity.
    Returns a similarity score between 0 and 1.
    """

    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    if image1 is None or image2 is None:
        return 0.0

    # Convert to HSV
    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

    # Histogram
    hist1 = cv2.calcHist(
        [hsv1],
        [0, 1],
        None,
        [50, 60],
        [0, 180, 0, 256]
    )

    hist2 = cv2.calcHist(
        [hsv2],
        [0, 1],
        None,
        [50, 60],
        [0, 180, 0, 256]
    )

    cv2.normalize(hist1, hist1)
    cv2.normalize(hist2, hist2)

    similarity = cv2.compareHist(
        hist1,
        hist2,
        cv2.HISTCMP_CORREL
    )

    # Keep value between 0 and 1
    similarity = max(0.0, min(1.0, similarity))

    return round(float(similarity), 3)