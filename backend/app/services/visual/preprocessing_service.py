import cv2


def preprocess_image(image_path):
    """
    Improve screenshot quality before OCR.
    """

    image = cv2.imread(image_path)

    if image is None:
        return image_path

    # -------------------------
    # Grayscale
    # -------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # -------------------------
    # CLAHE
    # -------------------------

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    gray = clahe.apply(gray)

    # -------------------------
    # Denoise
    # -------------------------

    gray = cv2.fastNlMeansDenoising(
        gray,
        None,
        10,
        7,
        21
    )

    # -------------------------
    # Sharpen
    # -------------------------

    kernel = [

        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]

    ]

    import numpy as np

    kernel = np.array(kernel)

    gray = cv2.filter2D(
        gray,
        -1,
        kernel
    )

    # -------------------------
    # Adaptive Threshold
    # -------------------------

    processed = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY,

        21,

        10

    )

    output = image_path.replace(".", "_processed.")

    cv2.imwrite(
        output,
        processed
    )

    return output