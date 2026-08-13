import cv2
import numpy as np


def calculate_layout_similarity(image1_path, image2_path):
    """
    Compare the structural layout of two screenshots.
    Returns a score between 0 and 1.
    """

    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    if image1 is None or image2 is None:
        return 0.0

    # Resize both images
    image1 = cv2.resize(image1, (800, 600))
    image2 = cv2.resize(image2, (800, 600))

    # Convert to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Edge Detection
    edge1 = cv2.Canny(gray1, 100, 200)
    edge2 = cv2.Canny(gray2, 100, 200)

    # Difference
    difference = cv2.absdiff(edge1, edge2)

    different_pixels = np.count_nonzero(difference)

    total_pixels = difference.shape[0] * difference.shape[1]

    similarity = 1 - (different_pixels / total_pixels)

    similarity = max(0.0, min(1.0, similarity))

    return round(float(similarity), 3)