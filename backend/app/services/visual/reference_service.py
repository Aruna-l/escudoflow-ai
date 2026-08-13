from pathlib import Path

REFERENCE_DIR = Path("vision/reference_brands")


def get_reference_images(brand):
    """
    Return every reference image
    for the detected brand.
    """

    if not brand or brand == "Unknown":
        return []

    folder = REFERENCE_DIR / brand.lower()

    if not folder.exists():
        return []

    images = []

    for ext in ("*.png", "*.jpg", "*.jpeg"):

        images.extend(folder.glob(ext))

    return images