import cv2
import numpy as np


def load_image(path: str):

    image = cv2.imread(path)

    if image is None:
        raise Exception(f"Unable to read image: {path}")

    return image


def resize_image(image, width=1280):

    h, w = image.shape[:2]

    if w <= width:
        return image

    ratio = width / w

    new_h = int(h * ratio)

    return cv2.resize(image, (width, new_h))


def to_gray(image):

    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def image_size(image):

    h, w = image.shape[:2]

    return w, h